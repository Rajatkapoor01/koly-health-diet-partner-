"use client"

import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Lightbulb } from "lucide-react"

interface SymptomSuggestionsProps {
  onSuggestionClick: (suggestion: string) => void
}

const symptomSuggestions = [
  "high blood pressure",
  "diabetes",
  "frequent headaches",
  "joint pain",
  "fatigue after meals",
  "digestive issues",
  "high cholesterol",
  "inflammation",
  "poor sleep quality",
  "low energy levels",
]

export function SymptomSuggestions({ onSuggestionClick }: SymptomSuggestionsProps) {
  return (
    <div className="space-y-2">
      <Label className="text-sm text-gray-600 flex items-center gap-2">
        <Lightbulb className="h-3 w-3" />
        Common Symptoms (click to add):
      </Label>
      <div className="flex flex-wrap gap-2">
        {symptomSuggestions.map((suggestion) => (
          <Button
            key={suggestion}
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => onSuggestionClick(suggestion)}
            className="h-7 text-xs text-gray-600 hover:text-gray-900 hover:bg-gray-100"
          >
            + {suggestion}
          </Button>
        ))}
      </div>
    </div>
  )
}
