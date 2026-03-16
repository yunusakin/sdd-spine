import { findSpectraRoot } from "../lib/runtime.js";
import { initializeFeatureBundle } from "../lib/specs.js";
import { next, ok, title } from "../lib/output.js";
import { parseOptions } from "../lib/options.js";

function featureInitCommand(argv) {
  const { options, positional } = parseOptions(argv, {
    booleanFlags: ["--help"],
    stringFlags: ["--cwd", "--name", "--owner", "--type"]
  });

  if (options["--help"]) {
    title(
      "Usage: spectra feature init <feature-id> [--name <display-name>] [--owner <owner>] [--type <assistant|api|service|web|worker|cli>] [--cwd <path>]"
    );
    return 0;
  }

  const featureId = positional[0];
  if (!featureId) {
    throw new Error("Missing required argument: <feature-id>");
  }

  const repoRoot = findSpectraRoot(options["--cwd"] ?? process.cwd());
  if (!repoRoot) {
    throw new Error(`Could not find a Spectra runtime from ${options["--cwd"] ?? process.cwd()}`);
  }

  const result = initializeFeatureBundle(repoRoot, {
    featureId,
    name: options["--name"] ?? null,
    owner: options["--owner"] ?? "product",
    type: options["--type"] ?? "assistant"
  });

  ok(`Created feature bundle: ${result.featureId}`);
  next(`spectra context --role planner --goal discover`);
  next("spectra validate");
  return 0;
}

export { featureInitCommand };
