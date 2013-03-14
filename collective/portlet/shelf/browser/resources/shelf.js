jq(document).ready(function () {
    var shelfs = jq('.shelf');
    shelfs.each( function(index) {
        var shelf = this;
        var cat_controls = jq(shelf).find('.subCategory');
        cat_controls.click(function (e) {
            e.preventDefault();
            var classes = jq(this).attr('class').split(' ');
            var category_id = '';
            for (i=0; i<classes.length; i++){
                if (classes[i].search('shelfc') != -1) {
                    category_id = classes[i];
                }
            }
            jq(shelf).find('div.'+category_id).show();
            initControls();
            var sections = jq(shelf).find(".category_section");
            sections.each( function(idx) {
                if (jq(this).attr('class').search(category_id) === -1){
                    jq(this).hide();
                }
            });
    });
    });

    var initControls = function(){
        var sections = jq(".category_section");
        sections.each( function(i) {
            var section= this;
            var scrollable = jq(section).find(".shelfScrollable");
            var scrollable_width = jq(scrollable).width();         
            if (scrollable_width !=0) {
                var elems = jq(scrollable).find('.scrollItem');
                var all_elems_width = 0;
                for (i=0; i<elems.length; i++) {   
                    all_elems_width = all_elems_width + jq(elems[i]).width();
                };
                if (scrollable_width > all_elems_width) {
                    jq(section).find('.browse, .scrollNavi').hide();

                }
           }; 
        });
    };

    initControls();
    var api = jq("div.shelfScrollable").scrollable({
        size: 1,
        clickable: false,
        loop: true
    }).navigator({indexed: true, navi: '.scrollNavi'}).pager();
});
