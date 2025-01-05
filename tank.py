from random import randint
TRIALS = 10000

def find_median(lst):
    n = len(lst)
    s = sorted(lst)
    return (s[n//2-1]/2.0+s[n//2]/2.0, s[n//2])[n % 2] if n else None

def count_between(lst, lower_bound, upper_bound):
    return len(list(filter(lambda x: lower_bound <= x <= upper_bound, lst)))

def find_mean(lst):
    return sum(lst)/len(lst)


def find_sd(lst):
    mean = sum(lst) / len(lst) 
    variance = sum([((x - mean) ** 2) for x in lst]) / len(lst) 
    return variance ** 0.5

def generate_sample(n=100, ss=7):
    population = list(range(1,n+1))
    sample = []
    for _ in range(0,ss):
        choice = population.pop(randint(0,len(population)-1))
        sample.append(choice)
    return sample

def test_strategy(strategy=None, n=100, plot=False, _print=False, fixed_ss = None, params = None):
    predictions = []
    for i in range(TRIALS):

        if fixed_ss:
            sample_size = fixed_ss
        else:
            sample_size = randint(int(n*0.05), int(n*0.2))

        sample = generate_sample(n=n, ss=sample_size)
        mean = find_mean(sample)
        sd = find_sd(sample)
        median = find_median(sample) 
        _max = max(sample)
        predictions.append(strategy(mean = mean, sd = sd, median = median, _max = _max, ss = sample_size, params = params))

    if _print:
        display(lst=predictions, strategy=strategy, n=n)

    return predictions


def distribution_data(lst):
    return find_mean(lst), find_median(lst), find_sd(lst)


def display(lst, n=100):
    mean, median, sd = distribution_data(lst)
    # source = getsource(strategy).split(':')[1].strip('\n')
    # print(f"strategy: {source}")
    string = f"mean error: {round(n-mean,3)} ({round(((n-mean)/n)*100,3)}%), median error: {round(n-median,3)} ({round(((n-median)/n)*100,3)}%), standard deviation: {round(sd,3)} ({round((sd/n)*100, 3)}%)\nprobablity of within 5%: {round(score_distribution(lst),3)}"
    return string


def score_distribution(lst, n=100):
    return count_between(lst, n*0.95, n*1.05)/TRIALS
