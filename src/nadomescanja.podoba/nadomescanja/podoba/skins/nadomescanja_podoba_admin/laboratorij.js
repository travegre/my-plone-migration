$(document).ready(function() {
    
 
  
  $('.ArchetypesInAndOutWidget').each(function() {
      $(this).find('table').parent().css({width:'100%'}); 
      $(this).find('table td').css({width:'50%'});
      $(this).find('table td select').css({width:'100%'}); 
      $(this).find('table').css({width:'100%'}); 
      $(this).find('table').parent().next().css({width:'50%'});
      $(this).find('table').parent().next().children('select').css({width:'100%'});

      
      $(this).find('div:first').before('<div><form id="kaj-' + $(this).attr('id') + '">Filter: <input name="filter-' + $(this).attr('id') + '" id="filter-' + $(this).attr('id') + '" value="" maxlength="30" size="30" type="text"></form></div>');

      $("#filter-" + $(this).attr('id')).keyup(function() {
        console.log(this.value)
        $.uiTableFilter( $(this).parent().parent().parent().find('table:first-child'), this.value );
      })
  });

  
  
  $('.field.ArchetypesInAndOutWidget').css({'width':'48%', 'margin-right':'1%', 'float':'left', 'clear':'none'});
  $('.field.ArchetypesInAndOutWidget label').css({'font-size':'1.5em'});
  $('#archetypes-fieldname-title').css({'width':'100%'});
  $('.field.ArchetypesInAndOutWidget table tr td:nth-child(2)').css({'display':'none'});


  

  



            	
           
            
            
            
});
