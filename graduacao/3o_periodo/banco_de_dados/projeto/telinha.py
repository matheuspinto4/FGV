from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Button, Input, Static
from textual.widgets import DataTable
import sqlite3

class DBApp(App):
    CSS_PATH = None
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        self.container = Container()
        yield self.container

    async def on_mount(self) -> None:
        await self.show_main_menu()

    async def show_main_menu(self):
        await self.container.remove_children()
        menu = Vertical(
            Button("Inserir Usuário", id="insert"),
            Button("Visualizar Usuários", id="view"),
            Button("Excluir Usuário", id="delete"),
            Button("Sair", id="exit")
        )
        await self.container.mount(menu)

    async def handle_button_pressed(self, message: Button.Pressed) -> None:
        btn_id = message.button.id
        if btn_id == "insert":
            await self.show_insert_form()
        elif btn_id == "view":
            await self.show_users()
        elif btn_id == "delete":
            await self.show_delete_form()
        elif btn_id == "exit":
            self.exit()

    async def show_insert_form(self):
        await self.container.remove_children()
        self.name_input = Input(placeholder="Nome", id="name")
        self.email_input = Input(placeholder="E-mail", id="email")
        submit = Button("Salvar", id="do_insert")
        await self.container.mount(Vertical(self.name_input, self.email_input, submit))

    async def show_delete_form(self):
        await self.container.remove_children()
        self.delete_input = Input(placeholder="ID do usuário", id="user_id")
        submit = Button("Excluir", id="do_delete")
        await self.container.mount(Vertical(self.delete_input, submit))

    async def show_users(self):
        await self.container.remove_children()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        rows = cursor.fetchall()
        conn.close()

        table = DataTable()
        table.add_columns("ID", "Nome", "E-mail")
        for row in rows:
            table.add_row(*map(str, row))

        back = Button("Voltar", id="back")
        await self.container.mount(Vertical(table, back))

    async def handle_button_pressed(self, message: Button.Pressed) -> None:
        btn_id = message.button.id
        if btn_id == "do_insert":
            name = self.name_input.value
            email = self.email_input.value
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            conn.close()
            await self.show_main_menu()
        elif btn_id == "do_delete":
            user_id = self.delete_input.value
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            await self.show_main_menu()
        elif btn_id == "back":
            await self.show_main_menu()

if __name__ == "__main__":
    # Inicializa o banco se não existir
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    app = DBApp()
    app.run()
