import { cn } from "@/lib/utils";

interface MessageBlockProps {
  iconComponent: React.ElementType;
  title: string;
  description: string;
  className?: string;
}

export function MessageBlock({
  iconComponent: IconComponent,
  title,
  description,
  className,
}: MessageBlockProps) {
  return (
    <div className={cn("text-center space-y-3", className)}>
      <div className="mx-auto w-16 h-16 bg-primary/20 text-primary rounded-full flex items-center justify-center">
        <IconComponent className="h-8 w-8" />
      </div>
      <h3 className="text-xl font-semibold text-foreground">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  );
}
