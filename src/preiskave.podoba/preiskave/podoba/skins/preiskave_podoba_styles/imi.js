function zapri() {
            
                if (!$("#hitri ul").hasClass('cez')) 
                {
                    $("#hitri ul").removeClass('cez');
                    $("#hitri ul").slideUp();
                }
            }

$(document).ready(function() {
$('.slika_popup').magnificPopup({type:'image'});

    $("#slider ul").carouFredSel({

					circular: true,
						scroll    : {
								duration  : 1500										
						},

					auto    : false,
					prev    : {
								button  : "#foo2_prev",
								key     : "left"
						},
						next    : {
								button  : "#foo2_next",
								key     : "right"
						},


	});
           
    $("#hit").click(function() {                
        $("#hitri ul").slideDown();
    });    
    
    $("#hitri ul").mouseleave(function () {
        $(this).removeClass('cez');
        $(this).slideUp();
    });
    
    $("#hitri ul").mouseover(function () {
        $(this).addClass('cez');
    });
    
    $("#hit").mouseleave(function () {
        
        setTimeout("zapri()", 1000);
    });
            
            
            	
            	

            	
	/*$("#prva_levo_zgor_zgori").carousel({ 
	    autoSlide: true,
	    effect: 'fade',
	    dispItems: 1,
	    animSpeed: 500,
	    autoSlideInterval: 8000          
	});*/
	
	$("#carousel").jshowoff({
	    autoPlay: true,
	    hoverPause: true,
	    changeSpeed: 2000,
	    speed: 8000
	});
	
	$(".jshowoff-slidelinks a").text('');
	$(".jshowoff-controls").hide();

	

    $(".podrocje_fajli h4").click(function() {                
        if (!$(this).hasClass('odprt')) 
        {
            $(this).addClass('odprt');
            $(this).nextAll('.ostali_fajli').slideDown();
        }
        else 
        {
            $(this).removeClass('odprt');
            $(this).nextAll('.ostali_fajli').slideUp();
        }
    });
     
            
            
            
    $(".naslov_vzorca").click(function() {                
        if (!$(this).hasClass('odprt')) 
        {
            $(this).addClass('odprt');
            $(this).nextAll('.ostali_fajli').slideDown();
        }
        else 
        {
            $(this).removeClass('odprt');
            $(this).nextAll('.ostali_fajli').slideUp();
        }
    });  
    
    
    $('.div_vzorci div').tsort('h4');
    
/*
    $(".naslov_vzorca:first").addClass('odprt');
    $(".naslov_vzorca:first").nextAll('.ostali_fajli').slideDown();
  */  
    
    $('.podrocje_skrito ul > li').tsort();
    $('.izbirnik_crk > li').tsort();
    $('.izbirnik_crk.2 > li').tsort();
    $('.crke_skrito').tsort('[class]');
    $('.crke_skrito ul li a').tsort('[title]');
    $('.crke_skrito.preiskave ul li').tsort();
    
    
    $('#drobtine span[dir]:last').before($('#vrinjen_bred'));
            
            
            
            
            
           
            
            
    $(".preiskave_crke").click(function() { 
       if (!$(this).hasClass('odprt')) 
       {
            id = $(this).attr('id');
            $(".preiskave_crke.odprt").removeClass('odprt');
            $(this).addClass('odprt');
            $(".crke_skrito").addClass('zaprto');
            $(".crke_skrito").removeClass('odprto');
            $(".crke_skrito." + id).removeClass('zaprto');
            $(".crke_skrito." + id).fadeOut();
            $(".crke_skrito." + id).addClass('odprto');
            
            $(".crke_skrito.zaprto:visible").fadeOut(function() {
                $(".crke_skrito.odprto").fadeIn();
            });
            
       }
       else
       {
            $(this).removeClass('odprt');
            $(".crke_skrito").removeClass('zaprto');
            $(".crke_skrito.odprto:visible").fadeOut(function() {
                $(".crke_skrito").fadeIn();
            });
            
       }
    });
            
            
            
            
            
    /* search forma skenslavanje */
    
    $('form#searchform .field:nth-child(4)').hide();  
    $('form#searchform .field:nth-child(7)').hide();  
    $('form#searchform .field:nth-child(8)').hide();       
    
    
    
    /* PREDMETI */
    
    
    $(".pedagoskavec a").click(function() {                
        $(this).nextAll('.ostali_fajli').slideDown();
        
        if (!$(this).hasClass('odprt')) 
        {
            $(this).addClass('odprt');
            $(this).text('prvih 5 obvestil');
            $(this).parent().nextAll('.ostali_fajli').slideDown();
        }
        else 
        {
            $(this).removeClass('odprt');
            $(this).text('vsa obvestila');
            $(this).parent().nextAll('.ostali_fajli').slideUp();
        }
    });
            
            
            
            
    /* HITRO ISKANJE */
            
          

	
    $('#okolo #searchGadget').focus(); 
					
					
   
	  
	  
    $('#listing_preiskav.vzorci div.razvrsti').tsort();

    dol = $('#listing_preiskav.vzorci div.razvrsti').length;
    st = dol / 3;
    ost = dol % 3;
    stevec = 0;

    $('#listing_preiskav.vzorci div.razvrsti').each(function () {
        if (stevec < st){
            $('#listing_preiskav.vzorci div.ena').append($(this));
            stevec++;
        }
        else if (stevec == st && ost > 0){
            $('#listing_preiskav.vzorci div.ena').append($(this));
        }
        else if (stevec < st*2){
            $('#listing_preiskav.vzorci div.dva').append($(this));
          stevec++;
        }
        else if (stevec == st*2 && ost > 1){
            $('#listing_preiskav.vzorci div.dva').append($(this));
        }
        else{
            $('#listing_preiskav.vzorci div.tri').append($(this));
            stevec++;
        }
    });
	 
    $('#okolo #searchGadget').bind('keyup', 'backspace', function(){
        if ($(this).val().length < 2){
            $(".rezultati").hide();
        } 
    });
   
      
    $('#okolo #searchGadget').live("keyup", function(e) {
        if ($(this).val().length > 1){
            $(".rezultati").show();
	    }	
	 });
	 
    $('#okolo #searchGadget').live("focus", function(e) {	
        if ($(this).val().length > 1){
            $(".rezultati").show();
	    }	
	 });
	 
	 			
	$(".podstran_preiskava .documentActions").clone().appendTo($('#podstran_preiskava_print'));		   


    


	//prikazovanje gumba Prikazi vec, ko je opis dolg več kot 5 vrstic
    if ($("#opis_preiskave").height() > 54){
	$(".podstran_preiskava.opis").addClass("hideContent");
	$(".show-more").show();	
    }

	//skrivanje in prikazovanje polnega opisa preiskave
    $(".show-more a").click(function(e) {
	e.preventDefault();
        var $this = $(this); 
        var $opis = $this.parent().prev("div.opis");
        var linkText = $this.text().toUpperCase();   

        if(linkText === "PRIKAŽI VEČ"){
            linkText = "Prikaži manj";
            $opis.addClass('showContent');
            $opis.removeClass('hideContent');
            //$opis.switchClass("hideContent", "showContent", 400);
        }
        else {
            linkText = "Prikaži več";
            $opis.addClass("hideContent");
            $opis.removeClass("showContent");
            //$opis.switchClass("showContent", "hideContent", 400);
        };

        $this.text(linkText); 
    });


/*
    $('#gumb_pokazi_vec').click(function(e) {
        e.stopPropagation();

        $('#opis_preiskave').css({
            'height': 'auto'
        })
        $(this).text('Pokaži manj');
    });

    $(document).click(function() {
        $('#opis_preiskave').css({
            'height': '50px'
        })
        $('#gumb_pokazi_vec').text('Pokaži več');
    })

         */   
            
            
            
});
