import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import subprocess
import os

class Converter(Gtk.Window):
    def __init__(self):
        super().__init__(title="Suncat Audio Converter")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        self.files = []

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.select_button = Gtk.Button(label="Select Video Files")
        self.select_button.connect("clicked", self.on_file_select)
        vbox.pack_start(self.select_button, False, False, 0)

        self.selected_files_label = Gtk.Label(label="No files selected")
        vbox.pack_start(self.selected_files_label, False, False, 0)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(separator, False, True, 5)

        label = Gtk.Label(label="Select output Audio")
        vbox.pack_start(label, False, False, 0)

        self.combo = Gtk.ComboBoxText()
        self.combo.append_text("pcm_s16le")
        self.combo.append_text("aac")
        self.combo.set_active(0)
        vbox.pack_start(self.combo, False, False, 0)

        self.button = Gtk.Button(label="Convert")
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_convert)
        vbox.pack_start(self.button, False, False, 0)

        self.status = Gtk.Label()
        vbox.pack_start(self.status, False, False, 0)

        self.button_box = Gtk.Box(spacing=6)
        self.more_button = Gtk.Button(label="Convert More")
        self.more_button.connect("clicked", self.on_convert_more)
        self.quit_button = Gtk.Button(label="Quit")
        self.quit_button.connect("clicked", Gtk.main_quit)
        self.button_box.pack_start(self.more_button, True, True, 0)
        self.button_box.pack_start(self.quit_button, True, True, 0)
        self.button_box.set_visible(False)
        self.more_button.set_sensitive(False)
        vbox.pack_start(self.button_box, False, False, 0)

    def on_file_select(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Select Video Files",
            parent=self,
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
        )
        dialog.set_select_multiple(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.files = dialog.get_filenames()
            files_text = "\n".join([os.path.basename(f) for f in self.files])
            self.selected_files_label.set_text(f"Selected files:\n{files_text}")
        else:
            self.files = []
            self.selected_files_label.set_text("No files selected")

        dialog.destroy()
        self.button.set_sensitive(bool(self.files))

    def on_convert(self, widget):
        if not self.files:
            self.status.set_text("No files selected.")
            return

        codec = self.combo.get_active_text()
        yes_to_all = False

        for f in self.files:
            output_dir = os.path.join(os.path.dirname(f), "Converted")
            os.makedirs(output_dir, exist_ok=True)
            out_name = os.path.splitext(os.path.basename(f))[0] + "_converted" + os.path.splitext(f)[1]
            output = os.path.join(output_dir, out_name)

            if os.path.exists(output) and not yes_to_all:
                dialog = Gtk.MessageDialog(
                    parent=self,
                    flags=0,
                    message_type=Gtk.MessageType.QUESTION,
                    buttons=Gtk.ButtonsType.NONE,
                    text=f"{out_name} exists. Overwrite?",
                )
                dialog.add_buttons(
                    "No", Gtk.ResponseType.NO,
                    "Yes", Gtk.ResponseType.YES,
                    "Yes to All", Gtk.ResponseType.APPLY
                )
                response = dialog.run()
                dialog.destroy()
                if response == Gtk.ResponseType.NO:
                    continue
                elif response == Gtk.ResponseType.APPLY:
                    yes_to_all = True

            if os.path.exists(output):
                try:
                    os.remove(output)
                except Exception:
                    self.status.set_text(f"Error removing file: {out_name}")
                    continue

            proc = subprocess.run(
                ["ffmpeg", "-i", f, "-c:v", "copy", "-c:a", codec, output],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if proc.returncode == 0:
                self.status.set_markup(f'Conversion complete. <a href="file://{output_dir}">Open Folder</a>')
                self.more_button.set_sensitive(True)
            else:
                self.status.set_text(f"Failed: {os.path.basename(f)}")

        self.button.set_sensitive(False)
        self.button_box.set_visible(True)
        self.button_box.set_margin_top(10)

    def on_convert_more(self, widget):
        self.files = []
        self.selected_files_label.set_text("No files selected")
        self.status.set_text("")
        self.button.set_sensitive(False)
        self.more_button.set_sensitive(False)
        self.button_box.set_visible(False)


win = Converter()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

