import { MessageCirclePlus, FolderKanban } from "lucide-react";
import {
  Tooltip,
  TooltipTrigger,
  TooltipContent,
} from "@/components/ui/tooltip";

export default function Sidebar() {
  return (
    <div className="w-80 h-screen bg-[#0c0d0c] text-white flex flex-col p-4">
      
      {/* Sidebar Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="w-9 h-9 bg-white text-center rounded-full font-bold font-sans text-black flex items-center justify-center">
          NAI
        </div>
        <div className="flex-1 ml-4 flex items-center justify-between">
          <span className="font-medium font-sans text-lg">Chat History</span>
          <Tooltip>
            <TooltipTrigger asChild>
              <button className="p-1 hover:bg-zinc-800 rounded">
                <MessageCirclePlus className="w-7 h-7" />
              </button>
            </TooltipTrigger>
            <TooltipContent className="bg-[#0c0d0c] text-white">
              <p className="text-sm">New Chat</p>
            </TooltipContent>
          </Tooltip>
        </div>
      </div>

      {/* Workspace */}
      <div className="mb-4">
        <div className="font-serif text-[13px] uppercase text-zinc-400 mb-4">
          Workspace
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-lg">
            <FolderKanban />
          </span>
          <span className="text-white font-sans">Workspace</span>
        </div>
      </div>

      {/* Chats Header */}
      <div className="flex items-center justify-between font-serif text-[13px] uppercase text-zinc-400 mb-4 mt-2">
        <span>Chats</span>
      </div>

      {/* Chats are hidden for now */}

      {/* Spacer */}
      <div className="flex-grow" />
    </div>
  );
}
