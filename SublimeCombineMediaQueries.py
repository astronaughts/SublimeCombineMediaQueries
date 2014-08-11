import sublime
import sublime_plugin
import subprocess
import os

SETTINGS_FILE = "SublimeCombineMediaQueries.sublime-settings"


class ScmqCombineCommand(sublime_plugin.WindowCommand):

    def run(self, path):
        settings = sublime.load_settings(SETTINGS_FILE)
        bin_path = settings.get("bin_path")
        if bin_path and os.environ["PATH"].find(bin_path) == -1:
            os.environ["PATH"] = bin_path + ":" + os.environ["PATH"]

        def combine(url):
            command = ["group-css-media-queries", url, url]
            try:
                shell = os.name == "nt"
                proc = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=shell,
                )
                out, err = proc.communicate()
                sublime.status_message("combined.")
            except:
                sublime.error_message("Error: Please specify a CSS file. - " + url)

        sublime.set_timeout(lambda: combine(path))


class ScmqFileCombineCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        self.window.run_command("scmq_combine", {"path": view.file_name()})
