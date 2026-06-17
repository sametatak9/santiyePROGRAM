import customtkinter as ctk
from tkinter import messagebox

from ui_theme import UI


class ModernCrudFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        db,
        table_name,
        title,
        subtitle,
        fields,
        list_columns,
        order_by="created_at",
        defaults=None,
    ):
        super().__init__(master, fg_color=UI.BG)
        self.db = db
        self.table_name = table_name
        self.title = title
        self.subtitle = subtitle
        self.fields = fields
        self.list_columns = list_columns
        self.order_by = order_by
        self.defaults = defaults or {}
        self.entries = {}
        self.records = []
        self.selected_id = None

        self._build()
        self.listele()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.left = ctk.CTkFrame(
            self,
            fg_color=UI.SURFACE,
            corner_radius=UI.RADIUS_LG,
            border_width=1,
            border_color=UI.BORDER,
        )
        self.left.grid(row=0, column=0, sticky="nsew", padx=(0, 9), pady=0)

        self.right = ctk.CTkFrame(
            self,
            fg_color=UI.SURFACE,
            corner_radius=UI.RADIUS_LG,
            border_width=1,
            border_color=UI.BORDER,
        )
        self.right.grid(row=0, column=1, sticky="nsew", padx=(9, 0), pady=0)

        header = ctk.CTkFrame(self.left, fg_color=UI.PRIMARY, corner_radius=UI.RADIUS_LG)
        header.pack(fill="x", padx=12, pady=12)

        ctk.CTkLabel(
            header,
            text=self.title,
            font=(UI.FONT, 18, "bold"),
            text_color="white",
            anchor="w",
        ).pack(fill="x", padx=14, pady=(12, 2))

        ctk.CTkLabel(
            header,
            text=self.subtitle,
            font=(UI.FONT, 11),
            text_color="#DBEAFE",
            anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 12))

        form = ctk.CTkScrollableFrame(self.left, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        for label, key, kind, values in self.fields:
            ctk.CTkLabel(
                form,
                text=label,
                font=(UI.FONT, 11, "bold"),
                text_color=UI.TEXT,
                anchor="w",
            ).pack(fill="x", pady=(8, 3))

            if kind == "combo":
                widget = ctk.CTkComboBox(form, values=values or [], height=36)
                if values:
                    widget.set(values[0])
            elif kind == "text":
                widget = ctk.CTkTextbox(form, height=88, border_width=1, border_color=UI.BORDER)
            else:
                widget = ctk.CTkEntry(form, height=36, border_color=UI.BORDER)

            widget.pack(fill="x")
            self.entries[key] = widget

        btns = ctk.CTkFrame(self.left, fg_color="transparent")
        btns.pack(fill="x", padx=12, pady=12)

        ctk.CTkButton(
            btns,
            text="Kaydet",
            height=38,
            fg_color=UI.PRIMARY,
            hover_color=UI.PRIMARY_HOVER,
            command=self.kaydet,
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkButton(
            btns,
            text="Temizle",
            height=38,
            fg_color=UI.TEXT_MUTED,
            hover_color="#475569",
            command=self.temizle,
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))

        list_header = ctk.CTkFrame(self.right, fg_color="transparent")
        list_header.pack(fill="x", padx=12, pady=(12, 8))

        ctk.CTkLabel(
            list_header,
            text="Kayitlar",
            font=(UI.FONT, 17, "bold"),
            text_color=UI.TEXT,
        ).pack(side="left")

        self.count_label = ctk.CTkLabel(
            list_header,
            text="0 kayit",
            height=26,
            corner_radius=UI.RADIUS_SM,
            fg_color=UI.SURFACE_SOFT,
            text_color=UI.TEXT_MUTED,
            font=(UI.FONT, 11, "bold"),
        )
        self.count_label.pack(side="right")

        self.search_entry = ctk.CTkEntry(
            self.right,
            placeholder_text="Ara...",
            height=38,
            border_width=0,
            fg_color=UI.SURFACE_SOFT,
        )
        self.search_entry.pack(fill="x", padx=12, pady=(0, 8))
        self.search_entry.bind("<KeyRelease>", lambda _event: self.listele())

        self.list_frame = ctk.CTkScrollableFrame(self.right, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def _widget_value(self, key):
        widget = self.entries[key]
        if isinstance(widget, ctk.CTkTextbox):
            return widget.get("0.0", "end").strip()
        return widget.get().strip()

    def _set_widget_value(self, key, value, kind=None):
        widget = self.entries[key]
        value = "" if value is None else str(value)
        if isinstance(widget, ctk.CTkTextbox):
            widget.delete("0.0", "end")
            widget.insert("0.0", value)
        elif kind == "combo":
            widget.set(value)
        else:
            widget.delete(0, "end")
            widget.insert(0, value)

    def _payload(self):
        data = dict(self.defaults)
        for _label, key, _kind, _values in self.fields:
            value = self._widget_value(key)
            data[key] = None if value == "" else value
        return data

    def kaydet(self):
        data = self._payload()
        ok, result = self.db.generic_kaydet(self.table_name, data, self.selected_id)
        if not ok:
            messagebox.showerror("Hata", str(result))
            return
        messagebox.showinfo("Kaydedildi", "Kayit basariyla kaydedildi.")
        self.temizle()
        self.listele()

    def temizle(self):
        self.selected_id = None
        for _label, key, kind, values in self.fields:
            widget = self.entries[key]
            if isinstance(widget, ctk.CTkTextbox):
                widget.delete("0.0", "end")
            elif kind == "combo" and values:
                widget.set(values[0])
            else:
                widget.delete(0, "end")

    def listele(self):
        self.records = self.db.generic_listele(self.table_name, self.order_by)
        q = self.search_entry.get().lower() if hasattr(self, "search_entry") else ""

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        shown = 0
        for record in self.records:
            haystack = " ".join(str(record.get(key, "")) for _label, key in self.list_columns).lower()
            if q and q not in haystack:
                continue
            self._record_row(record)
            shown += 1

        self.count_label.configure(text=f"{shown} kayit")

    def _record_row(self, record):
        row = ctk.CTkFrame(
            self.list_frame,
            fg_color=UI.SURFACE,
            corner_radius=UI.RADIUS_MD,
            border_width=1,
            border_color=UI.BORDER,
        )
        row.pack(fill="x", pady=5)

        text_block = ctk.CTkFrame(row, fg_color="transparent")
        text_block.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        first_label, first_key = self.list_columns[0]
        ctk.CTkLabel(
            text_block,
            text=str(record.get(first_key, "-")),
            font=(UI.FONT, 13, "bold"),
            text_color=UI.TEXT,
            anchor="w",
        ).pack(fill="x")

        detail_parts = []
        for label, key in self.list_columns[1:]:
            value = record.get(key)
            if value not in (None, ""):
                detail_parts.append(f"{label}: {value}")

        ctk.CTkLabel(
            text_block,
            text=" | ".join(detail_parts) or first_label,
            font=(UI.FONT, 10),
            text_color=UI.TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", pady=(2, 0))

        ctk.CTkButton(
            row,
            text="Ac",
            width=64,
            height=30,
            fg_color=UI.SURFACE_SOFT,
            text_color=UI.PRIMARY,
            hover_color="#E2E8F0",
            command=lambda r=record: self.kaydi_ac(r),
        ).pack(side="right", padx=8)

    def kaydi_ac(self, record):
        self.selected_id = record.get("id")
        for _label, key, kind, _values in self.fields:
            self._set_widget_value(key, record.get(key, ""), kind)
