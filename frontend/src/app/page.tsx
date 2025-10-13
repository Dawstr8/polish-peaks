import Image from "next/image";
import Link from "next/link";
import { Button } from "@/src/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/src/components/ui/card";
import { Badge } from "@/src/components/ui/badge";
import { Camera, MapPin, Cloud, Calendar, Mountain } from "lucide-react";
import peaksData from "@/src/data/sample-summit-photos.json";

export default function Home() {
  const peaks = peaksData;

  const features = [
    {
      id: 1,
      icon: Camera,
      title: "Upload Photos",
      description:
        "Upload photos from your mountain adventures. Our system automatically reads location and time data.",
    },
    {
      id: 2,
      icon: MapPin,
      title: "Auto Peak Detection",
      description:
        "Our system automatically matches your location to Polish mountain peaks and suggests the correct summit.",
    },
    {
      id: 3,
      icon: Cloud,
      title: "Weather History",
      description:
        "See the weather conditions from the day of your climb, making your memories more complete and informative.",
    },
  ];

  return (
    <>
      {/* Hero Section */}
      <section className="relative text-primary-foreground bg-gradient-to-b from-primary to-[var(--hero-gradient-to)]">
        <div className="absolute inset-0 overflow-hidden opacity-50">
          <div
            className="absolute inset-0 bg-[url('/mountains-pattern.svg')] bg-bottom bg-no-repeat"
            style={{ backgroundSize: "cover" }}
          ></div>
        </div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32 relative z-10">
          <div className="max-w-3xl">
            <h1 className="text-4xl sm:text-5xl font-bold tracking-tight mb-6">
              Document Your Mountain Adventures
            </h1>
            <p className="text-xl mb-8 text-primary-foreground/90">
              Track and share your conquests of Polish peaks with weather data,
              locations, and beautiful memories.
            </p>
            <div className="flex flex-wrap gap-4">
              <Button variant="secondary" asChild size="lg">
                <Link href="/upload">
                  <Camera className="w-4 h-4" />
                  Upload Your Summit
                </Link>
              </Button>
              <Button variant="outline" className="bg-invert" asChild size="lg">
                <Link href="/gallery">
                  <Mountain className="w-4 h-4" />
                  Explore Gallery
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4 text-foreground">
              How It Works
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Easily upload and organize your mountain adventures with smart
              features.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature) => (
              <Card key={feature.id}>
                <CardHeader>
                  <div className="w-12 h-12 bg-primary/15 text-primary rounded-full flex items-center justify-center mb-4">
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <CardTitle>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Gallery Preview Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-end mb-8">
            <h2 className="text-3xl font-bold text-foreground">
              Recent Adventures
            </h2>
            <Button variant="ghost" asChild>
              <Link href="/gallery">View all →</Link>
            </Button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {peaks.map((peak) => (
              <Card key={peak.id}>
                <div className="relative h-48">
                  <Image
                    src="/placeholder-mountain.svg"
                    alt={`${peak.name} summit`}
                    fill
                    className="object-cover"
                  />
                  <Badge className="absolute bottom-2 right-2 bg-background/90 text-foreground border border-border/60">
                    <MapPin className="w-3 h-3 mr-1" />
                    {peak.name}
                  </Badge>
                </div>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <CardTitle className="text-lg">{peak.title}</CardTitle>
                    <Badge variant="outline" className="text-xs">
                      <Calendar className="w-3 h-3 mr-1" />
                      {peak.date}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="flex gap-2 flex-wrap">
                    <Badge variant="secondary">
                      <Cloud className="w-3 h-3 mr-1" />
                      {peak.weather}
                    </Badge>
                    <Badge variant="secondary">
                      <Mountain className="w-3 h-3 mr-1" />
                      {peak.elevation}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary text-primary-foreground py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-6">
            Ready to document your mountain adventures?
          </h2>
          <p className="text-xl mb-8 max-w-3xl mx-auto text-primary-foreground/90">
            Join our community of mountain enthusiasts and start tracking your
            conquests of Polish peaks.
          </p>
          <Button size="lg" asChild variant="secondary">
            <Link href="/upload">
              <Camera className="w-4 h-4" />
              Upload Your First Summit
            </Link>
          </Button>
        </div>
      </section>
    </>
  );
}
