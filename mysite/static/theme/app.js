/*! AdminLTE 2.0.1 app.js
 * ======================
 * Main JS application file for AdminLTE v2. This file
 * should be included in all pages. It controls some layout
 * options and implements exclusive AdminLTE plugins.
 *
 * @Author  Almsaeed Studio
 * @Support <http://www.almsaeedstudio.com>
 * @Email   <support@almsaeedstudio.com>
 * @version 2.0
 * @license MIT <http://opensource.org/licenses/MIT>
 */

//Make sure jQuery has been loaded before app.js
if (typeof jQuery === "undefined") {
  throw new Error("AdminLTE requires jQuery");
}

'use strict';

/* AdminLTE
 *
 * @type Object
 * @description $.AdminLTE is the main object for the template's app.
 *				It's used for implementing functions and options related
 *				to the template. Keeping everything wrapped in an object
 *				prevents conflict with other plugins and is a better
 *				way to organize our code.
 */
$.AdminLTE = {};

/* --------------------
 * - AdminLTE Options -
 * --------------------
 * Modify these options to suit your implementation
 */
$.AdminLTE.options = {
  //Box Widget plugin options
  boxWidgetOptions: {
    boxWidgetIcons: {
      //The icon that triggers the collapse event
      collapse: 'fa fa-minus',
      //The icon that trigger the opening event
      open: 'fa fa-plus',
    },
    boxWidgetSelectors: {
      //Collapse button selector
      collapse: '[data-widget="collapse"]'
    }
  },
};

/* ------------------
 * - Implementation -
 * ------------------
 * The next block of code implements AdminLTE's
 * functions and plugins as specified by the
 * options above.
 */
$(function () {
  //Enable sidebar tree view controls
  $.AdminLTE.tree('.sidebar');

  $.AdminLTE.boxWidget.activate();

  /*
   * INITIALIZE BUTTON TOGGLE
   * ------------------------
   */
  $('.btn-group[data-toggle="btn-toggle"]').each(function () {
    var group = $(this);
    $(this).find(".btn").click(function (e) {
      group.find(".btn.active").removeClass("active");
      $(this).addClass("active");
      e.preventDefault();
    });

  });
});

/* ----------------------
 * - AdminLTE Functions -
 * ----------------------
 * All AdminLTE functions are implemented below.
 */


/* Tree()
 * ======
 * Converts the sidebar into a multilevel
 * tree view menu.
 *
 * @type Function
 * @Usage: $.AdminLTE.tree('.sidebar')
 */
$.AdminLTE.tree = function (menu) {
  $("li a", $(menu)).click(function (e) {
    //Get the clicked link and the next element
    var $this = $(this);
    var checkElement = $this.next();

    //Check if the next element is a menu and is visible
    if ((checkElement.is('.treeview-menu')) && (checkElement.is(':visible'))) {
      //Close the menu
      checkElement.slideUp('normal', function () {
        checkElement.removeClass('menu-open');
      });
      checkElement.parent("li").removeClass("active");
    }
    //If the menu is not visible
    else if ((checkElement.is('.treeview-menu')) && (!checkElement.is(':visible'))) {
      //Get the parent menu
      var parent = $this.parents('ul').first();
      //Close all open menus within the parent
      var ul = parent.find('ul:visible').slideUp('normal');
      //Remove the menu-open class from the parent
      ul.removeClass('menu-open');
      //Get the parent li
      var parent_li = $this.parent("li");

      //Open the target menu and add the menu-open class
      checkElement.slideDown('normal', function () {
        //Add the class active to the parent li
        checkElement.addClass('menu-open');
        parent.find('li.active').removeClass('active');
        parent_li.addClass('active');
      });
    }
    //if this isn't a link, prevent the page from being redirected
    if (checkElement.is('.treeview-menu')) {
      e.preventDefault();
    }
  });
};

/* BoxWidget
 * =========
 * BoxWidget is plugin to handle collapsing boxes from the screen.
 *
 * @type Object
 * @usage $.AdminLTE.boxWidget.activate()
 *Set all of your option in the main $.AdminLTE.options object
 */
$.AdminLTE.boxWidget = {
  activate: function () {
    var o = $.AdminLTE.options;
    var _this = this;
    //Listen for collapse event triggers
    $(o.boxWidgetOptions.boxWidgetSelectors.collapse).click(function (e) {
      e.preventDefault();
      _this.collapse($(this));
    });
  },
  collapse: function (element) {
    //Find the box parent
    var box = element.parents(".box").first();
    //Find the body and the footer
    var bf = box.find(".box-body, .box-footer");
    if (!box.hasClass("collapsed-box")) {
      //Convert minus into plus
      element.children(".fa-minus").removeClass("fa-minus").addClass("fa-plus");
      bf.slideUp(300, function () {
        box.addClass("collapsed-box");
      });
    } else {
      //Convert plus into minus
      element.children(".fa-plus").removeClass("fa-plus").addClass("fa-minus");
      bf.slideDown(300, function () {
        box.removeClass("collapsed-box");
      });
    }
  },
};
