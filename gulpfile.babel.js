import gulp from 'gulp';
import babel from 'gulp-babel';
import browserify from 'gulp-browserify';
import uglify from 'gulp-uglify';

const INPUT_FOLDER = "belt/static/src/";
const OUTPUT_FOLDER = "belt/static/js/";

gulp.task('default', function () {
    return gulp.src(`${INPUT_FOLDER}*.js`)
        .pipe(babel({
            presets: ['es2015']
        }))
        .pipe(browserify({
            insertGlobals: true,
            debug: false
        }))
        .pipe(uglify())
        .pipe(gulp.dest(OUTPUT_FOLDER));
});

gulp.task('watch', function () {
    gulp.watch(['src/admin/*.js'], ['default']);
});

gulp.task('build', ['default'], function () {
    return gulp.src(`${OUTPUT_FOLDER}*.js`)
        .pipe(uglify())
        .pipe(gulp.dest(OUTPUT_FOLDER));
});

