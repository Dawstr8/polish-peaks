import {
  Item,
  ItemContent,
  ItemDescription,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item";

interface MetadataItemProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

export function MetadataItem({ icon, title, description }: MetadataItemProps) {
  return (
    <Item>
      <ItemMedia className="h-full text-muted-foreground">{icon}</ItemMedia>
      <ItemContent>
        <ItemTitle className="text-sm font-medium text-muted-foreground">
          {title}:
        </ItemTitle>
        <ItemDescription className="text-base font-mono text-foreground">
          {description}
        </ItemDescription>
      </ItemContent>
    </Item>
  );
}
