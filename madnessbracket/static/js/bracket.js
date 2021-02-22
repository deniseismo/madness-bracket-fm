export class Bracket {
    constructor() {
        this.left = {};
        this.right = {};
        this.final = {};
    }
    setStructure(tracksLength) {
        const numberOfRounds = Math.log2(tracksLength / 2) * 2;
        let tracksPerRound = tracksLength / 2;
        for (let i = 0; i < numberOfRounds / 2; i ++) {
            this.left[i] = {};
            this.right[i] = {};
            for (let j = 0; j < tracksPerRound; j ++) {
                this.left[i][j] = null;
                this.right[i][j] = null;
            }
            tracksPerRound /= 2;
        }
        this.final['left'] = null;
        this.final['right'] = null;
        this.final['winner'] = null;
    }
}
