import { Check } from "lucide-react";

export function UploadSuccess() {
  return (
    <div className="text-center py-8">
      <div className="mx-auto w-16 h-16 mb-4 bg-primary/20 text-primary rounded-full flex items-center justify-center">
        <Check className="h-8 w-8" />
      </div>
      <h3 className="text-xl font-semibold mb-2 text-foreground">
        Upload Successful!
      </h3>
      <p className="text-muted-foreground mb-4">
        Your photo has been successfully uploaded.
      </p>
    </div>
  );
}
