"use client"

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertCircle } from "lucide-react"
import { useState } from "react"

export function ApiAlert() {
  const [isVisible, setIsVisible] = useState(true)

  // Optional: Add ability to dismiss the alert
  const handleDismiss = () => {
    setIsVisible(false)
  }

  return isVisible ? (
    <div className="fixed bottom-4 left-4 z-50 max-w-md animate-fade-in">
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <div className="flex justify-between items-start w-full">
          <div>
            <AlertTitle>Data Notice</AlertTitle>
            <AlertDescription>
              Some information on this website may be outdated. The original news source
              API source has discontinued its services.
            </AlertDescription>
          </div>
          <button
            onClick={handleDismiss}
            className="text-xs opacity-70 hover:opacity-100"
            aria-label="Dismiss"
          >
            ✕
          </button>
        </div>
      </Alert>
    </div>
  ) : null;
}
