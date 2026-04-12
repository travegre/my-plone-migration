$(document).ready(function() {

	
	  $('#searchGadget').focus(); 
		
		$('.kategorija.nad').click(function () {
	    if (! $(this).next().hasClass('open')) {
	    	$('.listing3.open').slideToggle(); 
		    $('.listing3.open').removeClass('open'); 
		    
		    $(this).next().slideToggle(); 
		    $(this).next().addClass('open');
		  }
	  });			
					
   $('.kategorija.klik').click(function () {
	    $('#searchGadget').val($(this).text());
	    $('#searchGadget').focus();
	  }); 
	  
	  
	 $('#listing div.razvrsti').tsort();
	 
	 dol = $('#listing div.razvrsti').length;
	 st = dol / 3;
	 ost = dol % 3;
	 stevec = 0;
	 
	 $('#listing div.razvrsti').each(function () {
	    if (stevec < st)
	    {
	      $('#listing div.ena').append($(this));
	      stevec++;
	    }
	    else if (stevec == st && ost > 0)
	    {
	      $('#listing div.ena').append($(this));
	    }
	    else if (stevec < st*2)
	    {
	      $('#listing div.dva').append($(this));
	      stevec++;
	    }
	    else if (stevec == st*2 && ost > 1)
	    {
	      $('#listing div.dva').append($(this));
	    }
	    else
	    {
	      $('#listing div.tri').append($(this));
	      stevec++;
	    }
	    
	 });
	 
	 $('#searchGadget').bind('keyup', 'backspace', function(){
        
        if ($(this).val().length < 2)
	      {
	        $(".rezultati").hide();
	      } 
   });
   
      
   $('#searchGadget').live("keyup", function(e) {
	  		
		  if ($(this).val().length > 1)
	    {
	        $(".rezultati").show();
	    } 
		  
		
	 });
	 
	 $('#searchGadget').live("focus", function(e) {
	  		
		  if ($(this).val().length > 1)
	    {
	        $(".rezultati").show();
	    } 
		  
		
	 });
	 
	 $("form").keypress(function(e) {
      if (e.which == 13) {
        return false;
      }
   });
	          	  					
				   

});


