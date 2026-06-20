import type { Metadata } from "next";
import "./globals.css";
import Nav from "@/components/Nav";

export const metadata: Metadata = {
  title: "Morning Paper — Личный кабинет",
  description: "Настройки, источники, стили, профиль интересов и выпуски вашей персональной газеты.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <body>
        <Nav />
        <main className="container">{children}</main>
      </body>
    </html>
  );
}
