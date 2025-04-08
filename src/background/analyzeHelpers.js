export function extractContentScore(data) {
    // all the categories, will have to add more later.
    const {
        nudity = {},
        offensive = {},
        gore = {},
        violence = {},
        selfharm = {},
        recreational_drug = {},
        alcohol = {},
        weapon = { classes: {} }
    } = data;

    return {
        sexual_activity: nudity.sexual_activity || 0,
        erotica: nudity.erotica || 0,
        firearm: weapon.classes.firearm || 0,
        alcohol: alcohol.prob || 0,
        drugs: recreational_drug.prob || 0,
        offensive: offensive.prob || 0,
        gore: gore.prob || 0,
        violence: violence.prob || 0,
        selfharm: selfharm.prob || 0
    }
}

export function isExplicitContent(scores, thresholds = {}) {
    return Object.entries(scores).some(([key, score]) => {
        const threshold = thresholds[key] ?? 0.95;
        return score > threshold;
    });
}