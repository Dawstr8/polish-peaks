import { useState } from "react";

export function useStepper(maxSteps: number) {
  const [step, setStep] = useState(0);

  const next = () => setStep((s) => Math.min(s + 1, maxSteps - 1));
  const back = () => setStep((s) => Math.max(s - 1, 0));

  return { step, next, back };
}
