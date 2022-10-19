from parsoda.model import Analyzer


class TwoFactionsPolarization(Analyzer):
    
    def analyze(self, data: dict):
        #print(f"[TwoFactionsPolarization] data: {data}")
        print('[TwoFactionsPolarization] data size: ' + str(len(data)))
        result = {}
        positives = 0
        negatives = 0
        for user in list(data.items()):
            if user[1] >= 0:
                positives += 1
            else:
                negatives += 1
        result["positive"] = positives
        result["negative"] = negatives
        return result


