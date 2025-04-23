// File: app/page.tsx
"use client";
import { useState } from "react";
import { Plus, Search, ArrowUp } from "lucide-react";
import Header from "../components/Header";

export default function MainWindow() {
  return (
    <div className="flex flex-col h-screen w-screen bg-[#161716] text-white">
      <Header />
      <ChatWindow />
      <SearchBar />
    </div>
  );
}

function ChatWindow() {
  const [selectedOption, setSelectedOption] = useState<string | null>(null);

  const options = [
    "Help me summarize case files",
    "Help me understand a legal document",
    "Find relevant laws and regulations",
  ];

  const handleOptionClick = (option: string) => {
    setSelectedOption(option);
  };

  return (
    <div className="flex-1 overflow-y-auto">
      <div
        className={`flex flex-col ${
          selectedOption
            ? "items-start mt-8"
            : "items-center justify-center h-full"
        } space-y-2 max-w-3xl mx-auto`}
      >
        {!selectedOption ? (
          <>
            <div className="flex flex-col items-center text-center">
              <div className="h-16 w-16 rounded-full bg-white flex items-center justify-center mb-4">
                <span className="text-2xl font-bold font-sans text-[#161716]">
                  NAI
                </span>
              </div>
              <h1 className="text-2xl font-sans font-medium mb-2">
                How can I help you?
              </h1>
            </div>

            <div className="w-full space-y-3">
              {options.map((option) => (
                <button
                  key={option}
                  className="w-full py-3 px-4 bg-[#1e1e1f] font-sans rounded-lg text-left hover:bg-neutral-700 transition"
                  onClick={() => handleOptionClick(option)}
                >
                  {option}
                </button>
              ))}
            </div>
          </>
        ) : (
          <>
            <div className="flex items-center gap-4">
              <div className="h-10 w-10 rounded-full bg-white flex items-center justify-center">
                <span className="text-sm font-bold text-[#161716]">NAI</span>
              </div>
              <p className="text-white font-sans text-base">{selectedOption}</p>
            </div>

            {(selectedOption === options[0] ||
              selectedOption === options[1]) && (
              <div className="w-full mt-2">
                <label className="block mb-2 font-sans">
                  Upload a document:
                </label>
                <input
                  type="file"
                  className="w-full bg-[#1e1e1f] text-white rounded p-2 border border-zinc-700"
                />
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

function SearchBar() {
  const [message, setMessage] = useState("");

  return (
    <div className="p-4">
      <div className="flex items-center bg-[#1e1e1f] rounded-[50px] p-2">
        <button className="flex items-center justify-center p-2 text-white">
          <Plus className="h-5 w-5" />
        </button>

        <div className="flex-1 mx-2 flex items-center">
          <textarea
            className="w-full bg-transparent resize-none font-sans outline-none text-white placeholder-gray-300 my-auto"
            placeholder="Send a Message"
            rows={1}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
        </div>

        <button className="flex items-center justify-center p-1.5 text-[#161716] bg-gray-300 rounded-full">
          {message.trim() === "" ? (
            <Search className="h-5 w-5" strokeWidth={2.5} />
          ) : (
            <ArrowUp className="h-5 w-5" strokeWidth={2.5} />
          )}
        </button>
      </div>
      <div className="flex items-center justify-center font-sans text-[12px] text-gray-300 mt-2">
        <span>
          NomosAI may provide inaccurate information. Always verify legal advice
          with qualified professionals.
        </span>
      </div>
    </div>
  );
}
