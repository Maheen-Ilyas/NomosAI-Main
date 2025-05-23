import React, { useState } from "react";
import { X } from "lucide-react";
import { motion } from "framer-motion";
import {
  Tooltip,
  TooltipTrigger,
  TooltipContent,
} from "@/components/ui/tooltip";
import { useRouter } from "next/navigation";

interface AuthenticationProps {
  isOpen: boolean;
  onClose: () => void;
}

const Authentication: React.FC<AuthenticationProps> = ({ isOpen, onClose }) => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [agreeToTerms, setAgreeToTerms] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true); // Start loading
  
    const endpoint = isSignUp ? "/api/auth/signup" : "/api/auth/signin";
    const payload = isSignUp
      ? { name: username, email, password }
      : { email, password };
  
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
  
      const data = await response.json();
      console.log("Response Data:", data); // Add this line
  
      if (!response.ok) throw new Error(data.error || "Authentication failed");

      if (data.token) localStorage.setItem("token", data.token);

      onClose();
      router.push("/dashboard");
    } catch (error: any) {
      console.error("Auth error:", error.message);
      alert(error.message);
    } finally {
      setIsLoading(false); // End loading
    }
  };  

  return (
    <div className="fixed inset-0 flex justify-center items-center z-50 bg-[#000814] bg-opacity-50">
      <motion.div
        className="bg-white rounded-xl w-[360px] p-6 shadow-xl"
        initial={{ opacity: 0, y: -100 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 100 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-serif font-bold text-[#000814]">
            {isSignUp ? "Sign Up" : "Sign In"}
          </h2>
          <button onClick={onClose} className="text-2xl text-[#000814] font-light">
            <X />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
          {isSignUp && (
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              className="border border-gray-300 px-4 py-2 rounded-md text-sm"
              disabled={isLoading} // 👈 Disable during load
              required
            />
          )}
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            className="border border-gray-300 px-4 py-2 rounded-md text-sm"
            disabled={isLoading}
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="border border-gray-300 px-4 py-2 rounded-md text-sm"
            disabled={isLoading}
            required
          />

          {isSignUp && (
            <label className="flex items-start space-x-2 text-sm text-gray-700">
              <input
                type="checkbox"
                checked={agreeToTerms}
                onChange={(e) => setAgreeToTerms(e.target.checked)}
                className="mt-1"
                disabled={isLoading}
              />
              <span>
                I understand and agree to the{" "}
                <Tooltip>
                  <TooltipTrigger asChild>
                    <a
                      href="/terms"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline text-[#000814] hover:text-blue-700"
                    >
                      Terms and Conditions
                    </a>
                  </TooltipTrigger>
                  <TooltipContent className="bg-[#0c0d0c] text-white">
                    <p className="text-sm">View the Terms and Conditions</p>
                  </TooltipContent>
                </Tooltip>
              </span>
            </label>
          )}

          <button
            type="submit"
            disabled={(isSignUp && !agreeToTerms) || isLoading}
            className={`py-2 text-white font-serif rounded-md transition-all flex items-center justify-center ${
              (isSignUp && !agreeToTerms) || isLoading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-[#000814] hover:bg-[#1a1a1a]"
            }`}
          >
            {isLoading ? (
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>{isSignUp ? "Creating..." : "Signing in..."}</span>
              </div>
            ) : isSignUp ? (
              "Create Account"
            ) : (
              "Sign In"
            )}
          </button>
        </form>

        <p className="text-sm text-center font-sans text-gray-600 mt-4">
          {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
          <button
            onClick={() => setIsSignUp(!isSignUp)}
            className="text-[#000814] font-sans font-semibold hover:underline ml-1"
            disabled={isLoading}
          >
            {isSignUp ? "Sign In" : "Sign Up"}
          </button>
        </p>
      </motion.div>
    </div>
  );
};

export default Authentication;
