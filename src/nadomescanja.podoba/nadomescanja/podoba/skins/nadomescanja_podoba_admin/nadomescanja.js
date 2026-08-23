/*jslint browser: true */
(function ($) {
    'use strict';

    /* prevent double execution if loaded twice */
    if (window._nadomescanjaLoaded) { return; }
    window._nadomescanjaLoaded = true;

    var labData   = {};
    var zaposleni = [];
    var rows      = [];

    /* -------------------------------------------------------- CSS -- */
    function injectStyles() {
        if ($('#nadomescanja-styles').length) { return; }
        $('<style id="nadomescanja-styles">').text([
            '#nadomescanja-ui {',
            '  margin: 1.5em 0;',
            '  padding: 1em;',
            '  background: #f8f8f8;',
            '  border: 1px solid #ddd;',
            '  border-radius: 3px;',
            '}',
            '#nadomescanja-ui h3 {',
            '  margin: 0 0 0.8em 0;',
            '  font-size: 1.1em;',
            '  color: #333;',
            '}',
            'table.nadomescanja-table {',
            '  width: 100%;',
            '  table-layout: fixed;',       /* prevents column jumping */
            '  border-collapse: collapse;',
            '}',
            'table.nadomescanja-table th {',
            '  background: #e8e8e8;',
            '  padding: 8px 10px;',
            '  text-align: left;',
            '  font-size: 1em;',
            '  border-bottom: 2px solid #ccc;',
            '}',
            'table.nadomescanja-table td {',
            '  padding: 6px 10px;',
            '  vertical-align: middle;',
            '  border-bottom: 1px solid #eee;',
            '}',
            /* fixed column widths — stops jumping */
            'table.nadomescanja-table th:nth-child(1),',
            'table.nadomescanja-table td:nth-child(1) { width: 30%; }',
            'table.nadomescanja-table th:nth-child(2),',
            'table.nadomescanja-table td:nth-child(2) { width: 25%; }',
            'table.nadomescanja-table th:nth-child(3),',
            'table.nadomescanja-table td:nth-child(3) { width: 35%; }',
            'table.nadomescanja-table th:nth-child(4),',
            'table.nadomescanja-table td:nth-child(4) { width: 10%; text-align: center; }',
            'table.nadomescanja-table select {',
            '  width: 100%;',
            '  font-size: 1em;',
            '  padding: 4px;',
            '  box-sizing: border-box;',
            '}',
            'td.nad-vodja-cell {',
            '  font-style: italic;',
            '  color: #555;',
            '  font-size: 1em;',
            '}',
            /* red visible delete button */
            'button.nad-del-btn {',
            '  background: #cc0000;',
            '  color: #fff;',
            '  border: none;',
            '  border-radius: 3px;',
            '  width: 28px;',
            '  height: 28px;',
            '  font-size: 1.4em;',
            '  line-height: 1;',
            '  cursor: pointer;',
            '  padding: 0;',
            '  display: inline-block;',
            '  vertical-align: middle;',
            '}',
            'button.nad-del-btn:hover { background: #990000; }',
            'button.nad-add-btn {',
            '  margin-top: 10px;',
            '  padding: 7px 16px;',
            '  font-size: 1em;',
            '}'
        ].join('\n')).appendTo('head');
    }

    /* -------------------------------------------------- data load -- */
    function loadServerData(callback) {
        var url = $('base').attr('href') + '@@nadomescanja-data-json';
        $.getJSON(url, function (data) {
            zaposleni = data.zaposleni || [];
            $.each(data.laboratoriji || [], function (i, lab) {
                labData[lab.id] = lab;
            });
            if (callback) { callback(); }
        });
    }

    /* ----------------------------------------- hidden field sync -- */
    function getHiddenField() {
        return $('input[name*="nadomescanja_json"]');
    }

    function loadRows() {
        var raw = getHiddenField().val();
        try { rows = JSON.parse(raw) || []; } catch (e) { rows = []; }
        /* backward compat — old format used nadomestni_vodja key */
        $.each(rows, function (i, row) {
            if (row.nadomestni_vodja !== undefined && !row.nadomestni_vodja_id) {
                row.nadomestni_vodja_id    = row.nadomestni_vodja;
                row.nadomestni_vodja_naziv = '';
                delete row.nadomestni_vodja;
            }
        });
    }

    function saveRows() {
        getHiddenField().val(JSON.stringify(rows));
    }

    /* ----------------------------------------------- row builder -- */
    function buildLabSelect(rowIndex, savedLabId) {
        var $sel = $('<select class="nad-lab-select">');
        $sel.append($('<option>').val('').text('-- laboratorij --'));
        $.each(labData, function (id, lab) {
            var $opt = $('<option>').val(id).text(lab.naziv);
            if (id === savedLabId) { $opt.attr('selected', 'selected'); }
            $sel.append($opt);
        });

        /* sort lab options alphabetically, keep placeholder first */
        $sel.find('option:not(:first)').tsort();
        $sel.change(function () {
            var lab_id = $(this).val();
            var lab    = labData[lab_id] || {};
            rows[rowIndex].laboratorij_id         = lab_id;
            rows[rowIndex].laboratorij_naziv      = lab.naziv        || '';
            rows[rowIndex].laboratorij_okrajsava  = lab.okrajsava    || '';
            rows[rowIndex].privzeti_vodja_id      = lab.vodja_id || '';
            rows[rowIndex].privzeti_vodja_naziv   = lab.vodja_naziv || '';
            rows[rowIndex].nadomestni_vodja_id    = '';
            rows[rowIndex].nadomestni_vodja_naziv = '';
            saveRows();
            updateRowCells($(this).closest('tr'), rows[rowIndex], rowIndex);
        });

        return $sel;
    }

    function buildNadSelect(rowIndex, lab, savedNadId) {
        var $sel = $('<select class="nad-nad-select">');
        $sel.append($('<option>').val('').text('-- nadomestnik --'));
        if (!lab) { return $sel; }
        $.each(zaposleni, function (i, z) {
            if (lab.vodja_id && z.id === lab.vodja_id) { return; }
            var $opt = $('<option>').val(z.id).text(z.naziv);
            if (z.id === savedNadId) { $opt.attr('selected', 'selected'); }
            $sel.append($opt);
        });

        /* sort people alphabetically, keep placeholder first */
        $sel.find('option:not(:first)').tsort();

        $sel.change(function () {
            var nad_id = $(this).val();
            var nad    = $.grep(zaposleni, function (z) { return z.id === nad_id; })[0] || {};
            rows[rowIndex].nadomestni_vodja_id    = nad_id;
            rows[rowIndex].nadomestni_vodja_naziv = nad.naziv || '';
            saveRows();
        });
        return $sel;
    }

    function updateRowCells($tr, rowData, rowIndex) {
        var lab = rowData.laboratorij_id
                ? (labData[rowData.laboratorij_id] || null)
                : null;
        $tr.find('td.nad-vodja-cell').text(getVodjaNaziv(lab));        /* always visible */
        $tr.find('td.nad-nad-cell').empty().append(
            buildNadSelect(rowIndex, lab, rowData.nadomestni_vodja_id)
        );
    }

    function getVodjaNaziv(lab) {
        if (!lab) { return '\u2014'; }
        return lab.vodja_naziv || lab.vodja_id || '\u2014';
    }

    function buildRow(rowIndex, rowData) {
        var lab = rowData.laboratorij_id
                ? (labData[rowData.laboratorij_id] || null)
                : null;
        var $tr = $('<tr>');

        $tr.append(
            $('<td class="nad-lab-cell">').append(
                buildLabSelect(rowIndex, rowData.laboratorij_id)
            )
        );
        $tr.append(
            $('<td class="nad-vodja-cell">').text(getVodjaNaziv(lab))
        );
        $tr.append(
            $('<td class="nad-nad-cell">').append(
                buildNadSelect(rowIndex, lab, rowData.nadomestni_vodja_id)  /* fixed */
            )
        );
        var $del = $('<button type="button" class="nad-del-btn">').html('&minus;')
            .click(function () {
                rows.splice(rowIndex, 1);
                saveRows();
                renderTable();
            });
        $tr.append($('<td class="nad-del-cell">').append($del));
        return $tr;
    }

    

    /* ----------------------------------------------- table render -- */
    function renderTable() {
        var $tbody = $('#nadomescanja-ui table tbody');
        $tbody.empty();
        $.each(rows, function (i, rowData) {
            $tbody.append(buildRow(i, rowData));
        });
    }

    /* ------------------------------------------------- UI builder -- */
    function buildUI() {
        if ($('#nadomescanja-ui').length > 0) { return; }

        injectStyles();

        var $wrapper = $('<div id="nadomescanja-ui">');
        $wrapper.append($('<h3>').text('Nadomescanja'));

        var $table = $('<table class="nadomescanja-table">')
            .append($('<thead>').append(
                $('<tr>')
                    .append($('<th>').text('Laboratorij'))
                    .append($('<th>').text('Privzeti vodja'))
                    .append($('<th>').text('Nadomestni vodja'))
                    .append($('<th>'))
            ))
            .append($('<tbody>'));
        $wrapper.append($table);

        var $addBtn = $('<button type="button" class="context nad-add-btn">').text('+ Dodaj nadomescanje')
            .click(function () {
                rows.push({
                    laboratorij_id:          '',
                    laboratorij_naziv:       '',
                    laboratorij_okrajsava:   '',
                    privzeti_vodja_id:    '',
                    privzeti_vodja_naziv:    '',
                    nadomestni_vodja_id:     '',
                    nadomestni_vodja_naziv:  ''
                });
                saveRows();
                renderTable();
            });
        $wrapper.append($('<p>').append($addBtn));

        /* insert before save/cancel buttons */
        var $formControls = $('.formControls').first();
        if ($formControls.length) {
            $formControls.before($wrapper);
            return;
        }
        /* fallbacks if .formControls not found */
        var $form = getHiddenField().closest('form');
        if ($form.length) { $form.append($wrapper); return; }
        getHiddenField().parent().after($wrapper);
    }

    /* -------------------------------------------------------- init -- */
    $(document).ready(function () {
        if (getHiddenField().length === 0) { return; }
        loadServerData(function () {
            loadRows();
            buildUI();
            renderTable();
        });
    });

}(jQuery));