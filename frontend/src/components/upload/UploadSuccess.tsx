import { MessageBlock } from "@/components/common/MessageBlock";
import { Check } from "lucide-react";

export function UploadSuccess() {
  return (
    <MessageBlock
      iconComponent={Check}
      title="Upload Successful!"
      description="Your photo has been successfully uploaded."
      className="py-8"
    />
  );
}
