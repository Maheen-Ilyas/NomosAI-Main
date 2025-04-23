"use client";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  return (
    <div className="relative flex flex-col items-center justify-center h-screen w-full">
      <h1 className="text-[80px] font-serif font-bold text-[#000814]">
        NomosAI
      </h1>
      <p className="mb-8 text-[26px] font-sans text-[#000814]">
        A platform for AI-powered Legal Analysis
      </p>
      <button 
      onClick={() => router.push("/dashboard")}
      className="px-3 py-2 text-[20px] font-medium font-sans rounded-[50px] text-[#000814] hover:text-[#FFFFFF] hover:bg-[#000814]">
        Get Started
      </button>
    </div>
  );
}
