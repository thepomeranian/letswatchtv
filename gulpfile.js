var gulp = require('gulp'),
    concat = require('gulp-concat'),
    scss = require('gulp-sass');
    livereload = require('gulp-livereload');
    
var PATHS = {
  BASE: {
    CSS: 'app/static/scss/'
  },
  DEST: {
    CSS: 'app/static/css/'
  }
};
gulp.task('default', ['css', 'watch', 'livereload']);
gulp.task('css', function() {
  gulp.src([PATHS.BASE.CSS + '*.scss'])
    .pipe(scss({outputStyle: 'compressed'}).on('error', scss.logError))
    .pipe(concat('main.css'))
    .pipe(gulp.dest(PATHS.DEST.CSS))
    .pipe(livereload());
});
gulp.task('watch', function() {
  gulp.watch([
    PATHS.BASE.CSS + '*.scss',
  ], ['css']);
});
gulp.task('livereload', function() {
  livereload.listen();
});