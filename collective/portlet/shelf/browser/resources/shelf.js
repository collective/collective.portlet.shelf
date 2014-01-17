jQuery(document).ready(function ($) {
    var shelfs = $('.shelf');
    shelfs.each(function (index) {
        var shelf = this;
        var cat_controls = $(shelf).find('.subCategory');
        cat_controls.click(function (e) {
            e.preventDefault();
            var classes = $(this).attr('class').split(' ');
            var category_id = '';
            for (i = 0; i < classes.length; i++) {
                if (classes[i].search('shelfc') != -1) {
                    category_id = classes[i];
                }
            }
            $(shelf).find('div.' + category_id).show();
            initControls();
            var sections = $(shelf).find(".category_section");
            sections.each(function (idx) {
                if ($(this).attr('class').search(category_id) === -1) {
                    $(this).hide();
                }
            });
        });
    });

    var initControls = function () {
        var sections = $(".category_section");
        sections.each(function (i) {
            var section = this;
            var scrollable = $(section).find(".shelfScrollable");
            var scrollable_width = $(scrollable).width();
            if (scrollable_width != 0) {
                var elems = $(scrollable).find('.scrollItem');
                var all_elems_width = 0;
                for (i = 0; i < elems.length; i++) {
                    all_elems_width = all_elems_width + $(elems[i]).width();
                };
                if (scrollable_width > all_elems_width) {
                    $(section).find('.browse, .scrollNavi').hide();

                }
            };
        });
    };

    initControls();
    var api = $("div.shelfScrollable").scrollable({
        size: 1,
        clickable: false,
        loop: true
    }).navigator({
        indexed: true,
        navi: '.scrollNavi'
    }).pager();
});
