# Adicionar Submódulo no repositorio principal

git submodule add https://github.com/seu-usuario/aln-projeto1.git graduacao/3o_periodo/algebra_linear_numerica/projetos/projeto1
git add .gitmodules graduacao/3o_periodo/algebra_linear_numerica/projetos/projeto1
git commit -m "Adicionado submódulo projeto1"
git push

# Clonar tudo:

git clone --recursive https://github.com/seu-usuario/faculdade.git


# Para atualizar tudo:

git submodule foreach git pull origin main


# Para Remover um submódulo:

git submodule deinit -f caminho/para/projeto
rm -rf .git/modules/caminho/para/projeto
git rm -f caminho/para/projeto