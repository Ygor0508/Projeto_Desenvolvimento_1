import type { Metadata } from 'next'
import './globals.css'
import { Toaster } from "@/components/ui/toaster" 

export const metadata: Metadata = {
  title: 'Robo_Trader',
  description: 'Dashboard para gerenciamento de robôs de trading',
  generator: 'Ygor Campos',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="pt-BR">
      <body className="dark"> 
        {children}
        <Toaster /> 
      </body>
    </html>
  )
}
