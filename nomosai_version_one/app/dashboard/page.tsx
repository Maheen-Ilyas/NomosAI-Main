"use client";
import Sidebar from "@/components/Sidebar";
import MainWindow from "@/components/MainWindow";
import { useState, useEffect } from "react";

export default function Dashboard() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <MainWindow/>
    </div>
  );
}

