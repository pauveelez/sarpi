var gulp = require("gulp"),
    stylus = require("gulp-stylus"),
    watch = require("gulp-watch"),
    livereload = require("gulp-livereload");
    concat = require("gulp-concat");
    uglify = require("gulp-uglify");


var sarpi = {
    stylus : {
        master : "./sarpi/static/stylus/estilos.styl",
        src : [
            "./sarpi/static/stylus/*.styl",
        ],
        dest : "./sarpi/static/css/",
    },
    js : {
        src : [
            "./sarpi/static/js/*.js",
        ],
        dest : "./sarpi/js/bundle/",
    },
    html : {
      src : [
        "./sarpi/templates/*.html",
      ]
    }
};

var nib = require('nib');
var rupture = require('rupture');

gulp.task('stylus', function () {
  gulp.src(sarpi.stylus.master)
    .pipe(stylus({
      use: [nib(), rupture()],
      import : 'nib',
      compress: true
    }))
    .pipe(gulp.dest(sarpi.stylus.dest))
    .pipe(livereload({auto:true}));
});

gulp.task('html', function(){
  gulp.src(sarpi.html.src)
  .pipe(livereload({auto:true}));
});


gulp.task('watch', function() {
  livereload.listen();
  gulp.watch(sarpi.stylus.src, ["stylus"]);
  gulp.watch(sarpi.html.src, ["html"]);
  gulp.watch(sarpi.js.src, ["html"]);
});

gulp.task('default', ['watch']);