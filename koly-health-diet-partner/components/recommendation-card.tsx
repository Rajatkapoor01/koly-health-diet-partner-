import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Shield, Sparkles, Target, Clock } from "lucide-react"

interface RecommendationCardProps {
  recommendation: {
    recommendation: string
    allergyMasked: string[]
    nutritionalHighlights: string[]
    safetyScore: number
    confidence: number
  }
  symptoms: string
  allergies: string[]
}

export function RecommendationCard({ recommendation, symptoms, allergies }: RecommendationCardProps) {
  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-green-700">
          <Target className="h-5 w-5" />
          Your Personalized Nutrition Plan
        </CardTitle>
        <CardDescription>
          AI-generated recommendations based on your health profile and trusted medical sources
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Main Recommendation */}
        <ScrollArea className="h-96 w-full rounded-md border p-4">
          <div className="prose prose-sm max-w-none">
            <div className="whitespace-pre-line text-gray-700 leading-relaxed">{recommendation.recommendation}</div>
          </div>
        </ScrollArea>

        {/* Nutritional Highlights */}
        {recommendation.nutritionalHighlights.length > 0 && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-semibold text-green-800 mb-3 flex items-center gap-2">
              <Sparkles className="h-4 w-4" />
              Key Nutritional Benefits
            </h4>
            <div className="grid gap-2">
              {recommendation.nutritionalHighlights.map((highlight, index) => (
                <div key={index} className="flex items-center gap-2 text-sm text-green-700">
                  <div className="w-2 h-2 bg-green-400 rounded-full flex-shrink-0" />
                  {highlight}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Allergy-Masked Items */}
        {recommendation.allergyMasked.length > 0 && (
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
            <h4 className="font-semibold text-orange-800 mb-3 flex items-center gap-2">
              <Shield className="h-4 w-4" />
              Allergy-Safe Filtering Applied
            </h4>
            <div className="space-y-2">
              {recommendation.allergyMasked.map((item, index) => (
                <div key={index} className="flex items-start gap-2 text-sm text-orange-700">
                  <Shield className="h-3 w-3 mt-0.5 flex-shrink-0" />
                  {item}
                </div>
              ))}
            </div>
            <div className="mt-3 text-xs text-orange-600">
              Your allergies ({allergies.join(", ")}) have been automatically filtered from all recommendations.
            </div>
          </div>
        )}

        {/* Timeline */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-semibold text-blue-800 mb-3 flex items-center gap-2">
            <Clock className="h-4 w-4" />
            Expected Timeline
          </h4>
          <div className="space-y-2 text-sm text-blue-700">
            <div className="flex justify-between">
              <span>Initial improvements</span>
              <Badge variant="outline" className="text-xs">
                1-2 weeks
              </Badge>
            </div>
            <div className="flex justify-between">
              <span>Significant changes</span>
              <Badge variant="outline" className="text-xs">
                4-6 weeks
              </Badge>
            </div>
            <div className="flex justify-between">
              <span>Full adaptation</span>
              <Badge variant="outline" className="text-xs">
                8-12 weeks
              </Badge>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
