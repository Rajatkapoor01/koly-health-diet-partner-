"use client"

import type React from "react"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Shield, X, Plus } from "lucide-react"

interface AllergyManagerProps {
  allergies: string[]
  onAllergiesChange: (allergies: string[]) => void
  disabled?: boolean
}

const commonAllergies = ["Dairy", "Gluten", "Nuts", "Peanuts", "Shellfish", "Fish", "Eggs", "Soy"]

export function AllergyManager({ allergies, onAllergiesChange, disabled }: AllergyManagerProps) {
  const [allergyInput, setAllergyInput] = useState("")

  const addAllergy = (allergy: string) => {
    const trimmedAllergy = allergy.trim().toLowerCase()
    if (trimmedAllergy && !allergies.includes(trimmedAllergy)) {
      onAllergiesChange([...allergies, trimmedAllergy])
      setAllergyInput("")
    }
  }

  const removeAllergy = (allergyToRemove: string) => {
    onAllergiesChange(allergies.filter((allergy) => allergy !== allergyToRemove))
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault()
      addAllergy(allergyInput)
    }
  }

  const addCommonAllergy = (allergy: string) => {
    addAllergy(allergy)
  }

  return (
    <div className="space-y-4">
      <Label className="flex items-center gap-2 text-base font-medium">
        <Shield className="h-4 w-4 text-orange-500" />
        Food Allergies & Intolerances
      </Label>

      <div className="flex gap-2">
        <Input
          placeholder="Type an allergy and press Enter (e.g., dairy, gluten, nuts)"
          value={allergyInput}
          onChange={(e) => setAllergyInput(e.target.value)}
          onKeyDown={handleKeyPress}
          onBlur={() => allergyInput.trim() && addAllergy(allergyInput)}
          disabled={disabled}
          className="flex-1"
        />
        <Button
          type="button"
          variant="outline"
          size="icon"
          onClick={() => addAllergy(allergyInput)}
          disabled={disabled || !allergyInput.trim()}
        >
          <Plus className="h-4 w-4" />
        </Button>
      </div>

      {/* Common Allergies */}
      <div className="space-y-2">
        <Label className="text-sm text-gray-600">Quick Add Common Allergies:</Label>
        <div className="flex flex-wrap gap-2">
          {commonAllergies.map((allergy) => (
            <Button
              key={allergy}
              type="button"
              variant="outline"
              size="sm"
              onClick={() => addCommonAllergy(allergy)}
              disabled={disabled || allergies.includes(allergy.toLowerCase())}
              className="h-8 text-xs"
            >
              {allergy}
            </Button>
          ))}
        </div>
      </div>

      {/* Current Allergies */}
      {allergies.length > 0 && (
        <div className="space-y-2">
          <Label className="text-sm text-gray-600">Your Allergies:</Label>
          <div className="flex flex-wrap gap-2">
            {allergies.map((allergy) => (
              <Badge key={allergy} variant="secondary" className="flex items-center gap-1 capitalize">
                <Shield className="h-3 w-3" />
                {allergy}
                <X className="h-3 w-3 cursor-pointer hover:text-red-500" onClick={() => removeAllergy(allergy)} />
              </Badge>
            ))}
          </div>
        </div>
      )}

      <div className="text-xs text-gray-500">
        All dietary recommendations will automatically exclude foods containing your listed allergies.
      </div>
    </div>
  )
}
