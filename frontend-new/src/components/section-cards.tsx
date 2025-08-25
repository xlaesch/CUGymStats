import { IconTrendingDown, IconTrendingUp } from "@tabler/icons-react"

import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardAction,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export function SectionCards() {
  return (
    <div className="grid grid-cols-1 gap-4 px-4 *:data-[slot=card]:shadow-xs lg:px-6 @xl/main:grid-cols-2 @5xl/main:grid-cols-4">
  <Card className="@container/card bg-gradient-to-t from-blue-50 to-blue-100">
        <CardHeader>
          <CardDescription>Helen Newman Fitness Center</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            29%
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
              <IconTrendingUp />
            </Badge>
          </CardAction>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">
            Last Count: 23
          </div>
          <div className="text-muted-foreground">
            Busier than usual
          </div>
        </CardFooter>
      </Card>
  <Card className="@container/card bg-gradient-to-t from-blue-50 to-blue-100">
        <CardHeader>
          <CardDescription>HNH Court 1 Basketball</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            42%
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
      <IconTrendingDown />
            </Badge>
          </CardAction>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">Last Count: 18</div>
          <div className="text-muted-foreground">Less busy than usual</div>
        </CardFooter>
      </Card>
  <Card className="@container/card bg-gradient-to-t from-orange-50 to-orange-100">
        <CardHeader>
          <CardDescription>HNH Court 2 Volleyball/Badminton</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            58%
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
      <IconTrendingDown />
            </Badge>
          </CardAction>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">Last Count: 24</div>
          <div className="text-muted-foreground">Less busy than usual</div>
        </CardFooter>
      </Card>
  <Card className="@container/card bg-gradient-to-t from-blue-50 to-blue-100">
        <CardHeader>
          <CardDescription>Noyes Court Basketball</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            12%
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
      <IconTrendingDown />
            </Badge>
          </CardAction>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">Last Count: 5</div>
          <div className="text-muted-foreground">Not busy</div>
        </CardFooter>
      </Card>
      {/* Second row */}
  <Card className="@container/card bg-gradient-to-t from-orange-50 to-orange-100">
        <CardHeader>
          <CardDescription>Noyes Fitness Center</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            65%
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
      <IconTrendingDown />
            </Badge>
          </CardAction>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">Last Count: 78</div>
          <div className="text-muted-foreground">Less busy than usual</div>
        </CardFooter>
      </Card>
  <Card className="@container/card bg-gradient-to-t from-blue-50 to-blue-100">
        <CardHeader>
          <CardDescription>Teagle Down Fitness Center</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            48%
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
      <IconTrendingDown />
            </Badge>
          </CardAction>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">Last Count: 52</div>
          <div className="text-muted-foreground">Less busy than usual</div>
        </CardFooter>
      </Card>
  <Card className="@container/card bg-gradient-to-t from-orange-50 to-orange-100">
        <CardHeader>
          <CardDescription>Teagle Up Fitness Center</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            83%
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
              <IconTrendingUp />
            </Badge>
          </CardAction>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">Last Count: 96</div>
          <div className="text-muted-foreground">Busier than usual</div>
        </CardFooter>
      </Card>
  <Card className="@container/card bg-gradient-to-t from-red-100 to-red-200 border-red-200">
        <CardHeader>
          <CardDescription>Toni Morrison Fitness Center</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            92%
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
              <IconTrendingUp />
            </Badge>
          </CardAction>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">Last Count: 110</div>
          <div className="text-muted-foreground">As busy as it gets</div>
        </CardFooter>
      </Card>
    </div>
  )
}
