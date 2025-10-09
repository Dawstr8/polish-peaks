import Image from "next/image";
import Link from "next/link";

export default function Logo() {
  return (
    <Link
      href="/"
      className="flex items-center hover:opacity-80 transition-opacity"
    >
      <Image
        src="/logo.svg"
        alt="Polish Peaks Mountains"
        width={55}
        height={35}
        priority
        className="h-7 w-auto mb-1"
      />
      <span className="ml-3 scroll-m-20 text-xl font-semibold tracking-tight text-primary">
        Polish Peaks
      </span>
    </Link>
  );
}
