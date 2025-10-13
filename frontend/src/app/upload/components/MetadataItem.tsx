interface MetadataItemProps {
  icon: React.ReactNode;
  label: string;
  value: string | React.ReactNode;
}

export function MetadataItem({ icon, label, value }: MetadataItemProps) {
  return (
    <div className="flex items-center gap-3">
      <div className="h-4 w-4 text-muted-foreground flex-shrink-0">{icon}</div>
      <div className="flex-1">
        <span className="text-sm font-medium text-muted-foreground">
          {label}:
        </span>
        <div className="text-foreground font-mono">{value}</div>
      </div>
    </div>
  );
}
