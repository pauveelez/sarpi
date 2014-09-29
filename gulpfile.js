var gulp = require("gulp"),
    stylus = require("gulp-stylus"),
    watch = require("gulp-watch"),
    livereload = require("gulp-livereload");


var sarpi = {
    stylus : {
        src : [
            "./sarpi/static/stylus/*.styl",
        ],
        dest : "./sarpi/static/css/",
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
  gulp.src(sarpi.stylus.src)
    .pipe(stylus({
      use: [nib(), rupture()],
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
});

gulp.task('default', ['watch']);