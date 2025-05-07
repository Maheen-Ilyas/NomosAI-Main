"use client";
import Sidebar from "@/components/Sidebar";
import MainWindow from "@/components/MainWindow";

export default function Dashboard() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <MainWindow/>
    </div>
  );
}

