$(document).ready(function() {
 
  
  $('.ArchetypesInAndOutWidget').each(function() {
      $(this).find('table').parent().css({width:'100%'}); 
      $(this).find('table td').css({width:'32%'});
      $(this).find('table td select').css({width:'100%'}); 
      $(this).find('table').css({width:'100%'}); 
      $(this).find('table').parent().next().css({width:'32%'});
      $(this).find('table').parent().next().children('select').css({width:'100%'});


      $(this).find('div:first').before('<div><form id="kaj-' + $(this).attr('id') + '">Filter: <input name="filter-' + $(this).attr('id') + '" id="filter-' + $(this).attr('id') + '" value="" maxlength="30" size="30" type="text"></form></div>');

      $("#filter-" + $(this).attr('id')).keyup(function(e) {
        //console.log(this.value);
        $.uiTableFilter( $(this).parent().parent().parent().find('table:first-child'), this.value );
        $(this).parent().parent().parent().find('table:first-child').children().children().children().children().scrollTop(0);
        if (e.keyCode == 40){
          $(this).parent().parent().parent().find('table:first-child').children().children().children().children().children(":first").attr("selected","selected");
          //$(this).parent().parent().parent().find('table:first-child').children().children().children().children().scrollTop(0);
        }
	     //$(this).find('table td').selected = !$(this).find('table td').selected;		
      })

      //ta stvar se NE DELUJE
      $(this).parent().parent().parent().find('table:first-child').children().children().children().children().focusin(function(){
        $(this).parent().parent().parent().find('table:first-child').children().children().children().children().children(":first").attr("selected","selected");
        $(this).parent().parent().parent().find('table:first-child').children().children().children().children().scrollTop(0);
        console.log("moglo bi bit poskrolano gor");  
    });
  });


  $('#archetypes-fieldname-dezurni_zdravnik').before('<div style="font-size: 30px; color: red; margin: 10px">DEŽURNA EKIPA</div>');
  $('#archetypes-fieldname-BOR').before('<div style="font-size: 30px; color: red; clear: both; margin: 10px">STANJE PRIPRAVLJENOSTI</div>');
  $('.field.ArchetypesInAndOutWidget').css({'width':'32%', 'margin-right':'1%', 'float':'left', 'clear':'none'});
  $('.field.ArchetypesInAndOutWidget table tr td:nth-child(2)').css({'display':'none'});
  



  $(window).keydown(function(event){
      if(event.keyCode == 13) {
        event.preventDefault();
      return false;
      }
  });

  //overwrite default Next navigationa...Ob kliku na Naslednji, se odpre tisto dežurstvo v edit mode-u
  //zaenkrat je to ok, ker nikjer drugje ne uporabljajo Next/Previous navigacije
  $( "a.next" ).click(function() {
    var link = $("a.next").attr("href");
    $("a.next").attr("href", link + '/edit');
    //alert(link);
  });  

  $('select').keyup(function(e) {
     //var prevCell = $(this).closest('td').prev();
     
     if (e.keyCode === 37) { //td tr tbody table div
      $(this).parent().parent().parent().parent().parent().parent().children().children().children().focus();
      //console.log($(this).children(":first").text());
      //$(this).parent().parent().children(":first").children().children(":first").attr("selected","selected");
      //console.log($(this).children(":first").text());
      
     }
  })
   

/* NE DELUJE
  $('.ui-state-default').click(function() {
    $('.gumb-uredi').focus();
  });
*/            
            
});
