import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import json
from collections import Counter

# Curated NICHE blogs - personal/enthusiast sites, NOT general news
TOPIC_URLS = {
    "Food": [
        "https://whattocook.substack.com/",
        "https://heresyourbite.substack.com/",
        "https://rouxgirl.substack.com/",
        "https://sundaystack.substack.com/",
        "https://jenneatsgoood.substack.com/",
        "https://www.playingwith.food/",
        "https://robertsimonson.substack.com/",
        "https://shakaylafelice.substack.com/",
        "https://barefoodtim.substack.com/",
        "https://saweeeties.substack.com/",
        "https://hannahwilding.substack.com/",
        "https://kristenfaitheats.substack.com/",
        "https://wellmadebykiley.substack.com/",
        "https://anastasiagladyr.substack.com/",
        "https://extrasharp.substack.com/",
        "https://alexandracooks.com/",
        "https://www.budgetbytes.com/",
        "https://smittenkitchen.com/",
        "https://pinchofyum.com/",
        "https://cookieandkate.com/",
        "https://www.loveandlemons.com/",
        "https://www.gimmesomeoven.com/",
        "https://www.thefullhelping.com/",
        "https://www.averiecooks.com/",
        "https://www.halfbakedharvest.com/",
        "https://veggiedesserts.com/",
        "https://minimalistbaker.com/",
        "https://www.onceuponachef.com/",
        "https://damndelicious.net/",
        "https://www.twopeasandtheirpod.com/",
        "https://sallysbakingaddiction.com/"
    ],
    "Music": [
        "https://santarosarecords.com/",
        "https://varioussmallflames.co.uk/",
        "https://obscuresound.com/",
        "https://www.indieshuffle.com/",
        "https://atwoodmagazine.com/",
        "https://www.alfitude.com/",
        "https://www.ear-to-the-ground.com/",
        "https://www.gorillavsbear.com/",
        "https://earmilk.com/",
        "https://www.cougarmicrobes.com/",
        "https://thissongissick.com/",
        "https://neonmusic.co.uk/",
        "https://www.thelineofbestfit.com/",
        "https://thewildhoneypie.com/",
        "https://indieisnotagenre.com/",
        "https://indiecentralmusic.com/",
        "https://aquariumdrunkard.com/",
        "https://fortheloveof bands.com/",
        "https://pigeonsandplanes.com/",
        "https://indiemusicfilter.com/",
        "https://ra.co/",
        "https://5mag.net/",
        "https://deephouseamsterdam.com/",
        "https://deepershadesofhouse.com/",
        "https://xlr8r.com/",
        "https://trommelmusic.com/",
        "https://www.electronicbeats.net/",
        "https://www.dancingastronaut.com/",
        "https://mixmag.net/",
        "https://magneticmag.com/",
        "https://edmtunes.com/"
    ],
    "Travel": [
        "https://walkingtheworld.substack.com/",
        "https://elizabethminchilli.substack.com/",
        "https://www.borderlessliving.com/",
        "https://tonihammersley.substack.com/",
        "https://johnkretschmer.substack.com/",
        "https://adventureswithsarah.substack.com/",
        "https://ridewithian.substack.com/",
        "https://francetraveller.substack.com/",
        "https://unpluggedtraveler.substack.com/",
        "https://lovescotland.substack.com/",
        "https://courageoustraveler.substack.com/",
        "https://thecatholictraveler.substack.com/",
        "https://sacredparis.substack.com/",
        "https://lastoria.substack.com/",
        "https://www.mappedandnoted.com/",
        "https://gettingaround.substack.com/",
        "https://letterfromiceland.substack.com/",
        "https://www.dreaminmiles.com/",
        "https://www.ourportugaljourney.com/",
        "https://outdoorwiseliving.substack.com/",
        "https://sotheresthisplace.substack.com/",
        "https://queerlybelovedtravel.substack.com/",
        "https://jetsetchristina.substack.com/",
        "https://www.brentandmichaelaregoingplaces.com/",
        "https://fathomwaytogo.substack.com/",
        "https://brooklynfamilytravelers.substack.com/",
        "https://emilychappell.substack.com/",
        "https://adrianlandin.substack.com/",
        "https://zenabirch.substack.com/",
        "https://jilloutside.substack.com/",
        "https://yolojournal.substack.com/"
    ],
    "Sport": [
        "https://billanddougosu.substack.com/",
        "https://thethistle1876.substack.com/",
        "https://dnlbenson.substack.com/",
        "https://tiggyvalen.substack.com/",
        "https://michaelpetalengro.substack.com/",
        "https://www.thesportsfanjournal.com/",
        "https://thechubbyrunner.com/",
        "https://runeatrepeat.com/",
        "https://www.dcrainmaker.com/",
        "https://hungryrunnergirl.com/",
        "https://www.scienceofrunning.com/?v=47e5dceea252",
        "https://iancorless.org/",
        "https://www.girlontheriver.com/",
        "https://strengthrunning.com/blog/",
        "https://believeintherun.com/",
        "https://www.just-football.com/",
        "https://www.thegolfblog.com/",
        "https://facts.net/lifestyle/sports/20-facts-about-tennis/",
        "https://runyoung50.co.uk/",
        "https://www.milebymileblog.com/",
        "https://relentlessforwardcommotion.com/",
        "https://runtothefinish.com/blog/",
        "https://www.runningwithattitude.com/",
        "https://tennisabides.com/",
        "https://www.sbnation.com/",
        "https://thesportsdaily.org/",
        "https://breakingmuscle.com/",
        "https://www.thegolfblog.com/",
        "https://facts.net/lifestyle/sports/20-facts-about-tennis/",
        "https://runyoung50.co.uk/",
        "https://www.milebymileblog.com/",
        "https://relentlessforwardcommotion.com/",
        "https://runtothefinish.com/blog/",
        "https://www.runningwithattitude.com/",
        "https://tennisabides.com/",
        "https://www.sbnation.com/",
        "https://thesportsdaily.org/",
        "https://breakingmuscle.com/",
        "https://www.khcoaching.com/?utm_campaign=profile_chips",
        "https://billrabinowitz.substack.com/?utm_campaign=profile_chips",
        "https://www.auburnobserver.com/?utm_campaign=profile_chips"
    ],
    "Literature": [
        "https://alittleblogofbooks.com/",
        "https://booksandbao.com/",
        "https://stephanieverni.com/",
        "https://fictionophile.com/",
        "https://www.whisperingstories.com/",
        "https://bookishbeck.com/",
        "https://www.thebooksatchel.com/",
        "https://thelitedit.com/",
        "https://booksbonesbuffy.com/",
        "https://pagesunbound.wordpress.com/",
        "https://www.notesinthemargin.org/",
        "https://booksaremyfavouriteandbest.com/",
        "https://readervoracious.com/",
        "https://thebookishlibra.com/",
        "https://novelgossip.com/",
        "https://dearauthor.com/",
        "https://www.bookishelf.com/",
        "https://literarypotpourri.com/",
        "https://readingladies.com/",
        "https://www.thebooksatchel.com/",
        "https://thelitedit.com/",
        "https://booksbonesbuffy.com/",
        "https://pagesunbound.wordpress.com/",
        "https://www.notesinthemargin.org/",
        "https://booksaremyfavouriteandbest.com/",
        "https://readervoracious.com/",
        "https://thebookishlibra.com/",
        "https://novelgossip.com/",
        "https://dearauthor.com/",
        "https://www.bookishelf.com/",
        "https://literarypotpourri.com/",
        "https://readingladies.com/",
        "https://shelleywilsonauthor.com/",
        "https://sunshineandbooksblog.com/",
        "https://rathertoofondofbooks.com/",
        "https://bookishbrews.com/",
        "https://badredheadmedia.com/blog/",
        "https://thetattooedbookgeek.wordpress.com/",
        "https://booksplease.org/",
        "https://leafingthroughlife.blogspot.com/",
        "https://reading-in-bed.com/",
        "https://www.literaryfeline.com/",
        "https://www.jennsbookshelves.com/"
    ]
}

def fetch_blog_keywords(url):
    """Fetch a blog and extract keywords using TextBlob."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()
        
        text = soup.get_text()
        
        # Use TextBlob to extract noun phrases (keywords)
        blob = TextBlob(text)
        phrases = [p.lower() for p in blob.noun_phrases if len(p) > 3]
        
        # Get sentiment
        sentiment = blob.sentiment.polarity
        
        return phrases, sentiment
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return [], 0.0

def train_topic_models():
    """Train topic models by analyzing blogs and extracting common keywords."""
    topic_models = {}
    
    for topic, urls in TOPIC_URLS.items():
        print(f"\nTraining {topic}...")
        all_keywords = []
        all_sentiments = []
        
        for url in urls:
            print(f"  Analyzing: {url}")
            keywords, sentiment = fetch_blog_keywords(url)
            all_keywords.extend(keywords)
            all_sentiments.append(sentiment)
        
        # Find most common keywords
        keyword_counts = Counter(all_keywords)
        top_keywords = [kw for kw, count in keyword_counts.most_common(50)]
        
        # Average sentiment
        avg_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0.0
        
        topic_models[topic] = {
            "keywords": top_keywords,
            "avg_sentiment": avg_sentiment
        }
        
        print(f"  Found {len(top_keywords)} keywords")
    
    # Save to JSON
    with open('topic_models.json', 'w') as f:
        json.dump(topic_models, f, indent=2)
    
    print("\nTopic models saved to topic_models.json")

if __name__ == "__main__":
    train_topic_models()
