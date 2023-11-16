import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QRadioButton, QVBoxLayout, QButtonGroup, QPushButton, QMessageBox

class FormularioInscricao(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Inscrições para Evento")
        self.setGeometry(250, 250, 700, 400)

        self.cadastros_realizados = 0
        self.cadastros_restantes = 50
        self.nomes_cadastrados = set()
        self.cadastros = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label_cadastros = QLabel("Não há cadastros")
        layout.addWidget(self.label_cadastros)

        self.nome_label = QLabel("Nome:")
        self.nome_input = QLineEdit()
        self.nome_input.setMaxLength(50)
        layout.addWidget(self.nome_label)
        layout.addWidget(self.nome_input)

        self.idade_label = QLabel("Idade:")
        self.idade_input = QLineEdit()
        self.idade_input.setMaxLength(3)
        layout.addWidget(self.idade_label)
        layout.addWidget(self.idade_input)

        self.endereco_label = QLabel("Endereço:")
        self.endereco_input = QLineEdit()
        self.endereco_input.setMaxLength(50)
        layout.addWidget(self.endereco_label)
        layout.addWidget(self.endereco_input)

        self.reside_sp_group = QButtonGroup(self)
        self.reside_sp_sim = QRadioButton("Sim")
        self.reside_sp_nao = QRadioButton("Não")
        self.reside_sp_group.addButton(self.reside_sp_sim, 1)
        self.reside_sp_group.addButton(self.reside_sp_nao, 2)
        layout.addWidget(QLabel("Reside em SP?"))
        layout.addWidget(self.reside_sp_sim)
        layout.addWidget(self.reside_sp_nao)

        self.disponibilidade_noite_group = QButtonGroup(self)
        self.disponibilidade_noite_sim = QRadioButton("Sim")
        self.disponibilidade_noite_nao = QRadioButton("Não")
        self.disponibilidade_noite_group.addButton(self.disponibilidade_noite_sim, 1)
        self.disponibilidade_noite_group.addButton(self.disponibilidade_noite_nao, 2)
        layout.addWidget(QLabel("Tem disponibilidade à noite?"))
        layout.addWidget(self.disponibilidade_noite_sim)
        layout.addWidget(self.disponibilidade_noite_nao)

        self.botao_cadastrar = QPushButton("Cadastrar")
        self.botao_cadastrar.clicked.connect(self.validar_cadastro)
        layout.addWidget(self.botao_cadastrar)

        self.setLayout(layout)

    def validar_cadastro(self):
        nome = self.nome_input.text()
        idade = self.idade_input.text()
        endereco = self.endereco_input.text()
        reside_sp = "Sim" if self.reside_sp_group.checkedButton() == self.reside_sp_sim else "Não"
        disponibilidade_noite = "Sim" if self.disponibilidade_noite_group.checkedButton() == self.disponibilidade_noite_sim else "Não"

        mensagens_erro = []

        if len(nome) < 3 or any(char.isdigit() for char in nome):
            mensagens_erro.append("O campo nome precisa ter pelo menos 3 caracteres e não pode conter números!")  
            
        try:
            idade = int(idade)
            if idade < 18:
                mensagens_erro.append("O evento é proibido para menores de 18 anos!")
        except ValueError:
            mensagens_erro.append("O campo idade precisa ser preenchido com um número inteiro!") 

        if len(endereco) < 4 or not any(char.isdigit() for char in endereco):
            mensagens_erro.append("O campo endereço precisa ser preenchido com nome da rua/avenida e o número de residência!") 

        if not self.reside_sp_group.checkedButton():
            mensagens_erro.append("Você precisa selecionar uma opção para campo 'Reside em SP?'!")

        if not self.disponibilidade_noite_group.checkedButton():
            mensagens_erro.append("Você precisa selecionar uma opção para o campo 'Tem disponibilidade à noite?'!")
            
        if nome in self.nomes_cadastrados:
            mensagens_erro.append("Este nome já foi cadastrado!")

        if len(mensagens_erro) == 0:
            if self.cadastros_realizados < 50:
                self.cadastros_realizados += 1
                self.cadastros_restantes -= 1
                self.nomes_cadastrados.add(nome)
                self.cadastros.append({'Nome': nome, 'Idade': idade, 'Endereço': endereco, 'Reside em SP': reside_sp, 'Disponibilidade à noite': disponibilidade_noite})
                QMessageBox.information(self, "Cadastro Validado", f"Cadastro validado com sucesso!\nVagas restantes: {self.cadastros_restantes}")
                self.nome_input.clear()
                self.idade_input.clear()
                self.endereco_input.clear()
                self.reside_sp_group.setExclusive(False)
                self.reside_sp_nao.setChecked(False)
                self.reside_sp_sim.setChecked(False)
                self.reside_sp_group.setExclusive(True)
                self.disponibilidade_noite_group.setExclusive(False)
                self.disponibilidade_noite_nao.setChecked(False)
                self.disponibilidade_noite_sim.setChecked(False)
                self.disponibilidade_noite_group.setExclusive(True)
            else:
                QMessageBox.warning(self, "As inscrições estão encerradas!")
        else:
            QMessageBox.warning(self, "Erro no Cadastro!", "\n".join(mensagens_erro))

        self.atualizar_label_cadastros()

    def atualizar_label_cadastros(self):
        if self.cadastros_realizados == 0:
            self.label_cadastros.setText("Não há cadastros!")
        else:
            self.label_cadastros.setText(f"Cadastros realizados: {self.cadastros_realizados}\nCadastros restantes: {self.cadastros_restantes}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    formulario = FormularioInscricao()
    formulario.show()
    sys.exit(app.exec_())
