$ErrorActionPreference = 'Stop'

# Set this to the number of Framsticks processes your machine can handle.
$Workers = 8
$RunsPerMutation = 10
$Generations = 1000
$Stagnation = 50
$Seed = 12345
$MutationValues = @('0', '005', '010', '020', '030', '040', '050')

Set-Location $PSScriptRoot
$LibraryPath = (Resolve-Path '..').Path

foreach ($Mutation in $MutationValues) {
    $Simulation = "eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;f9-mut-$Mutation.sim"
    $OutputPrefix = "results-f9-$Mutation"
    $HallOfFame = "HoF-f9-$Mutation-{run}.gen"

    Write-Host "========== STARTING MUTATION $Mutation ($RunsPerMutation runs, $Workers workers) =========="
    $Arguments = @(
        'FramsticksEvolution.py',
        '-path', $LibraryPath,
        '-sim', $Simulation,
        '-opt', 'vertpos',
        '-max_numparts', '30',
        '-max_numgenochars', '50',
        '-initialgenotype', '/*9*/BLU',
        '-popsize', '50',
        '-generations', $Generations,
        '-stagnation', $Stagnation,
        '-runs', $RunsPerMutation,
        '-workers', $Workers,
        '-seed', $Seed,
        '-hof_size', '1',
        '-hof_savefile', $HallOfFame,
        '-output_prefix', $OutputPrefix
    )

    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Mutation $Mutation failed with exit code $LASTEXITCODE"
    }
}

Write-Host 'All mutation settings completed.'
