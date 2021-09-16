<h1 align="center">
    <img src="https://ik.imagekit.io/gt1uvp8jacz/roit__Z2Myi-j6O.png?updatedAt=1631745438091">
</h1>
<h1 align="center">
    <img src="https://ik.imagekit.io/gt1uvp8jacz/roit_66I_rRDI5.png?updatedAt=1631745633748">
</h1>
<h1 align="center">
    <img src="https://ik.imagekit.io/gt1uvp8jacz/roit_uf3Y7T4Nj.png?updatedAt=1631745821939">
</h1>

# Índice

- [Sobre](#-sobre)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Como baixar o projeto](#-como-baixar-o-projeto)
- [Acessar Amazon AWS](#-acessar-amazon-aws)

---

## 🗒️ Sobre

Esse projeto tem como objetivo principal avaliar as skills do candidato referente as tecnologias abaixo:

**1.** Montar uma solução utilizando arquitetura de **autoencoder** capaz de limpar imagens disponibilizadas no dataset na pasta 1.dirty que se encontram com diversos ruídos e retornar no padrão em que se encontram na pasta 2. Cleaned document.

**2.** Montar uma **API** que seja capaz de receber uma imagem em base64 e retornar a imagem limpa em base64 com seu respectivo **OCR (Optical Character Recognition)** na resposta da API.

**3.** Guardar a imagem em base64 de entrada/saída em um **banco de dados**, além de outras informações que o candidato julgar necessário.

**4.** Encapsular a aplicação utilizando **Docker**. Disponibilizar **DockerFile**.

**5.** Hospedar o código em um repositório do github utilizando conceitos de **Gitflow e Commit**

---

## 🚀️ Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

- Python 3.9
- Flask Restful
- MongoDB
- Docker
- Tensorflow
- Tesseract

---

## 📁️ Como baixar o projeto 

```bash
    # Clonar o repositório
    $ git clone https://github.com/Duzanski/ia_ocr

    # Entrar no diretório
    $ cd ia_ocr

    # Instalar as dependências
    $ make install

    # Build Docker
    $ sudo docker-compose build

    # Start server
    $ sudo docker-compose up
```
---

## ☁️ Acessar Amazon AWS

```bash
    # URL
    ec2-3-22-97-79.us-east-2.compute.amazonaws.com:5000

    RESOURCE            ADDRES                  PROTOCOL        PARAM            RESPONSE/STATUS CODE
    GetImageCleaned     /getcleanedimage        POST            name             200 OK
                                                                image            Base64 cleaned image
                                                                                 String text


    GetString           /getstring              POST            name             200 OK
                                                                                 String text
    name = nome qualquer para a imagem
    image = imagem dirty em base 64
```
