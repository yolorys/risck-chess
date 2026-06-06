{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "risck-analysis-env";
  
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.pandas
    pkgs.python3Packages.chess
    pkgs.python3Packages.duckdb
  ];

  shellHook = ''
    echo "Environment Ready! Python, Pandas, Chess, and DuckDB are loaded."
  '';
}