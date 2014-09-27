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
    }
};

//var nib = require('nib');

gulp.task('stylus', function () {
  gulp.src(sarpi.stylus.src)
    .pipe(stylus({
      //use: nib(),
      compress: true
    }))
    .pipe(gulp.dest(sarpi.stylus.dest))
    .pipe(livereload({auto:true}));
});


gulp.task('watch', function() {
  livereload.listen();
  gulp.watch(sarpi.stylus.src, ["stylus"]);
});

gulp.task('default', ['watch']);