"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ExternalLink, FileText, Database, GraduationCap, Building } from "lucide-react"

interface Source {
  title: string
  url: string
  type: "pubmed" | "usda" | "eatright" | "harvard"
}

interface SourcesSectionProps {
  sources: Source[]
}

const sourceIcons = {
  pubmed: FileText,
  usda: Database,
  eatright: Building,
  harvard: GraduationCap,
}

const sourceColors = {
  pubmed: "text-blue-600 bg-blue-50 border-blue-200",
  usda: "text-green-600 bg-green-50 border-green-200",
  eatright: "text-purple-600 bg-purple-50 border-purple-200",
  harvard: "text-red-600 bg-red-50 border-red-200",
}

export function SourcesSection({ sources }: SourcesSectionProps) {
  return (
    <Card className="bg-gray-50 border-gray-200">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-gray-800">
          <ExternalLink className="h-5 w-5" />
          Trusted Medical Sources
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {sources.map((source, index) => {
          const Icon = sourceIcons[source.type]
          const colorClass = sourceColors[source.type]

          return (
            <div key={index} className={`border rounded-lg p-3 ${colorClass}`}>
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-start gap-3 flex-1">
                  <Icon className="h-4 w-4 mt-0.5 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <h5 className="font-medium text-sm leading-tight">{source.title}</h5>
                    <p className="text-xs opacity-75 mt-1 truncate">{source.url}</p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-8 w-8 p-0 flex-shrink-0"
                  onClick={() => window.open(source.url, "_blank")}
                >
                  <ExternalLink className="h-3 w-3" />
                </Button>
              </div>
            </div>
          )
        })}

        <div className="text-xs text-gray-500 mt-4 p-3 bg-white rounded border">
          <strong>Source Verification:</strong> All recommendations are based on peer-reviewed research from PubMed,
          official USDA nutritional data, Academy of Nutrition and Dietetics guidelines, and Harvard T.H. Chan School of
          Public Health publications.
        </div>
      </CardContent>
    </Card>
  )
}
