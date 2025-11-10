// import { type NextRequest, NextResponse } from "next/server"
// import crypto from "crypto"

// // Em um ambiente real, você usaria um banco de dados seguro
// const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || "your-32-character-secret-key-here"

// function encrypt(text: string): string {
//   const cipher = crypto.createCipher("aes-256-cbc", ENCRYPTION_KEY)
//   let encrypted = cipher.update(text, "utf8", "hex")
//   encrypted += cipher.final("hex")
//   return encrypted
// }

// export async function POST(request: NextRequest) {
//   try {
//     const { apiKey, secretKey } = await request.json()

//     if (!apiKey || !secretKey) {
//       return NextResponse.json({ error: "API Key e Secret Key são obrigatórios" }, { status: 400 })
//     }

//     // Criptografar as chaves antes de armazenar
//     const encryptedApiKey = encrypt(apiKey)
//     const encryptedSecretKey = encrypt(secretKey)

//     // Em um ambiente real, você salvaria no banco de dados
//     // Por enquanto, vamos simular o salvamento
//     console.log("Chaves API criptografadas e salvas:", {
//       apiKey: encryptedApiKey.substring(0, 10) + "...",
//       secretKey: encryptedSecretKey.substring(0, 10) + "...",
//     })

//     return NextResponse.json({
//       success: true,
//       message: "Chaves API configuradas com sucesso",
//     })
//   } catch (error) {
//     console.error("Erro ao configurar chaves API:", error)
//     return NextResponse.json({ error: "Erro interno do servidor" }, { status: 500 })
//   }
// }



// import { type NextRequest, NextResponse } from "next/server"
// import crypto from "crypto"

// // Chave de criptografia segura
// const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || "your-32-character-secret-key-here"
// const ALGORITHM = "aes-256-cbc"

// function encrypt(text: string): string {
//   try {
//     // Gerar IV aleatório
//     const iv = crypto.randomBytes(16)
    
//     // Criar cipher
//     const cipher = crypto.createCipheriv(ALGORITHM, Buffer.from(ENCRYPTION_KEY), iv)
    
//     // Criptografar
//     let encrypted = cipher.update(text, "utf8", "hex")
//     encrypted += cipher.final("hex")
    
//     // Retornar IV + dados criptografados
//     return iv.toString("hex") + ":" + encrypted
//   } catch (error) {
//     console.error("Erro na criptografia:", error)
//     throw new Error("Falha na criptografia")
//   }
// }

// function decrypt(encryptedData: string): string {
//   try {
//     const parts = encryptedData.split(":")
//     const iv = Buffer.from(parts[0], "hex")
//     const encrypted = parts[1]
    
//     const decipher = crypto.createDecipheriv(ALGORITHM, Buffer.from(ENCRYPTION_KEY), iv)
//     let decrypted = decipher.update(encrypted, "hex", "utf8")
//     decrypted += decipher.final("utf8")
    
//     return decrypted
//   } catch (error) {
//     console.error("Erro na descriptografia:", error)
//     throw new Error("Falha na descriptografia")
//   }
// }

// export async function POST(request: NextRequest) {
//   try {
//     const { apiKey, secretKey } = await request.json()

//     if (!apiKey || !secretKey) {
//       return NextResponse.json({ error: "API Key e Secret Key são obrigatórios" }, { status: 400 })
//     }

//     if (!ENCRYPTION_KEY || ENCRYPTION_KEY.length !== 32) {
//       return NextResponse.json({ error: "Chave de criptografia inválida. Deve ter 32 caracteres." }, { status: 500 })
//     }

//     // Criptografar as chaves antes de armazenar
//     const encryptedApiKey = encrypt(apiKey)
//     const encryptedSecretKey = encrypt(secretKey)

//     // Em um ambiente real, você salvaria no banco de dados
//     // Por enquanto, vamos salvar em variáveis de ambiente temporárias
//     process.env.ENCRYPTED_BINANCE_API_KEY = encryptedApiKey
//     process.env.ENCRYPTED_BINANCE_SECRET_KEY = encryptedSecretKey

//     console.log("✅ Chaves API criptografadas e salvas com sucesso")

//     return NextResponse.json({
//       success: true,
//       message: "Chaves API configuradas com sucesso",
//     })
//   } catch (error) {
//     console.error("Erro ao configurar chaves API:", error)
//     return NextResponse.json({ 
//       error: `Erro interno do servidor: ${error instanceof Error ? error.message : 'Erro desconhecido'}` 
//     }, { status: 500 })
//   }
// }

// // Função para recuperar chaves descriptografadas
// export function getDecryptedKeys() {
//   try {
//     const encryptedApiKey = process.env.ENCRYPTED_BINANCE_API_KEY
//     const encryptedSecretKey = process.env.ENCRYPTED_BINANCE_SECRET_KEY

//     if (!encryptedApiKey || !encryptedSecretKey) {
//       return null
//     }

//     return {
//       apiKey: decrypt(encryptedApiKey),
//       secretKey: decrypt(encryptedSecretKey)
//     }
//   } catch (error) {
//     console.error("Erro ao recuperar chaves:", error)
//     return null
//   }
// }





import { NextResponse } from "next/server"
import fs from "fs/promises"
import path from "path"
import os from "os"
import fernet from "fernet"

// O caminho para o arquivo de configuração
const CONFIG_DIR = path.join(os.homedir(), ".trading-bot-config")
const CONFIG_FILE_PATH = path.join(CONFIG_DIR, "api_keys.json.enc")

// Pega a chave do .env.local
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY

// Função de criptografia que USA FERNET
function encryptData(text: string, key: string): string {
  // A biblioteca 'fernet' é compatível com a chave do Python
  const secret = new fernet.Secret(key)
  const token = new fernet.Token({ secret })
  return token.encode(text) // Criptografa o texto
}

export async function POST(request: Request) {
  try {
    // 1. Validar a Chave de Criptografia
    if (!ENCRYPTION_KEY) {
      console.error("Erro Fatal: ENCRYPTION_KEY não definida no .env.local")
      return NextResponse.json(
        { error: "Chave de criptografia do servidor não definida." },
        { status: 500 }
      )
    }
    
    // 2. Obter dados que o usuário digitou na tela
    const { apiKey, secretKey } = await request.json()
    if (!apiKey || !secretKey) {
      return NextResponse.json(
        { error: "apiKey e secretKey são obrigatórias" },
        { status: 400 }
      )
    }

    // 3. Criar o objeto de configuração
    const configData = {
      binance_api_key: apiKey,
      binance_api_secret: secretKey,
    }

    // 4. Criptografar os dados usando FERNET
    const encryptedData = encryptData(
      JSON.stringify(configData),
      ENCRYPTION_KEY
    )

    // 5. Garantir que o diretório de configuração exista
    await fs.mkdir(CONFIG_DIR, { recursive: true })

    // 6. Salvar o arquivo criptografado
    await fs.writeFile(CONFIG_FILE_PATH, encryptedData)

    console.log(`Configuração salva com sucesso em: ${CONFIG_FILE_PATH}`)

    return NextResponse.json({
      success: true,
      message: "Chaves API configuradas e criptografadas com sucesso.",
    })
  } catch (error) {
    console.error("Erro ao salvar a configuração:", error)
    const errorMessage =
      error instanceof Error ? error.message : "Erro desconhecido"
    return NextResponse.json(
      { error: "Erro interno ao salvar configuração", details: errorMessage },
      { status: 500 }
    )
  }
}
