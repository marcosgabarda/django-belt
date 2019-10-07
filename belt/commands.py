import os


class ProgressBarCommand(object):
    """Mixin to add a progress bar to a management command."""

    default_terminal_size = 25
    progress_symbol = "="

    def terminal_size(self):
        """Gets the terminal columns size."""
        try:
            _, columns = os.popen("stty size", "r").read().split()
            return min(int(columns) - 10, 100)
        except ValueError:
            return self.default_terminal_size

    def bar(self, progress):
        """Shows on the stdout the progress bar for the given progress."""
        if not hasattr(self, "_limit") or not self._limit:
            self._limit = self.terminal_size()
        graph_progress = int(progress * self._limit)
        self.stdout.write("\r", ending="")
        progress_format = "[%-{}s] %d%%".format(self._limit)
        self.stdout.write(
            self.style.SUCCESS(
                progress_format
                % (self.progress_symbol * graph_progress, int(progress * 100))
            ),
            ending="",
        )
        self.stdout.flush()
