# GRIDLINE Resources — GitHub Pages

Este repositório serve os recursos obrigatórios do GRIDLINE por HTTPS usando GitHub Pages.

## Estrutura

```text
.
├── .nojekyll
├── index.html
├── resources.json
├── content/
│   └── music/
├── packages/
└── tools/
    └── build_resources.py
```

## 1. Crie o repositório

No GitHub, crie um repositório público chamado exatamente:

```text
gridline-resources
```

Envie o conteúdo desta pasta para a raiz do repositório.

## 2. Coloque os recursos

Coloque músicas e demais arquivos obrigatórios dentro de `content/`.

Exemplo:

```text
content/
└── music/
    ├── no_bad_news.ogg
    └── nothing_on_my_mind.ogg
```

## 3. Gere o ZIP, tamanho e SHA-256

No computador, dentro do repositório:

```bash
python tools/build_resources.py --version 1 --base-url https://SEU_USUARIO.github.io/gridline-resources
```

O script criará:

```text
packages/gridline_resources_v1.zip
```

e atualizará automaticamente `resources.json` com URL, tamanho em bytes e SHA-256.

Quando mudar qualquer arquivo obrigatório, aumente a versão:

```bash
python tools/build_resources.py --version 2 --base-url https://SEU_USUARIO.github.io/gridline-resources
```

## 4. Ative o GitHub Pages

No repositório:

1. `Settings`
2. `Pages`
3. Em `Build and deployment`, selecione `Deploy from a branch`
4. Branch: `main`
5. Pasta: `/(root)`
6. `Save`

Depois de publicado, teste:

```text
https://SEU_USUARIO.github.io/gridline-resources/resources.json
```

E o pacote:

```text
https://SEU_USUARIO.github.io/gridline-resources/packages/gridline_resources_v1.zip
```

## 5. Configure o Android

Nos arquivos Android fornecidos junto deste kit, altere apenas:

```java
public static final String CATALOG_URL =
        "https://SEU_USUARIO.github.io/gridline-resources/resources.json";
```

Também adicione ao `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

Use `StartupActivity` como LAUNCHER. Ela consulta o catálogo e decide se abre o jogo ou a instalação obrigatória.

## Atualizações

- Não altere uma versão que já foi publicada.
- Para recursos novos, gere `v2`, `v3`, etc.
- O app valida o SHA-256 antes de instalar.
- A instalação usa uma pasta temporária e só substitui os recursos antigos quando a extração termina.
- Depois de instalado, o pacote funciona offline.

## Limites práticos do GitHub

Mantenha cada ZIP abaixo de 100 MiB. Se passar de 25 MiB, envie pelo Git/GitHub Desktop, pois o upload pelo navegador tem um limite menor.

Para um jogo com tráfego grande, migre posteriormente os arquivos pesados para uma CDN/objeto storage e mantenha o mesmo formato de `resources.json`.
