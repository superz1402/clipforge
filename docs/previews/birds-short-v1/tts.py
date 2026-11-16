import asyncio, edge_tts, json, subprocess
V="en-US-AvaMultilingualNeural"
S=[("Bang! And every bird nearby vanishes in a heartbeat. Why?","+8%","+6Hz","+10%"),
("Because to a bird, that blast isn't a celebration. It's a predator attack!","+0%","+4Hz","+15%"),
("Its danger system fires, stress hormones flood in, and the body screams one thing: run.","+10%","+2Hz","+10%"),
("And panic spreads. One bird takes off, hundreds follow, because hesitating could be fatal.","+8%","+3Hz","+10%"),
("The closer the blast, the more of them bolt. Studies of mass takeoffs show it.","+4%","+3Hz","+5%"),
("At night it's even worse. They fly blind, crash into things, and burn energy they can't spare.","-8%","-4Hz","+0%"),
("So, if birds could vote, would they ban firecrackers... or just list humans as a natural disaster?","-2%","+4Hz","+5%")]
async def one(i,t,r,p,v):
    c=edge_tts.Communicate(t,V,rate=r,pitch=p,volume=v,boundary="WordBoundary")
    au=b'';ws=[]
    async for ch in c.stream():
        if ch['type']=='audio': au+=ch['data']
        elif ch['type']=='WordBoundary': ws.append((ch['offset']/1e7,ch['duration']/1e7,ch['text']))
    open(f's{i}.mp3','wb').write(au); return ws
async def main():
    starts=[];out=[];off=0.0;gaps=[0.25,0.3,0.25,0.3,0.3,0.35,0]
    lst=[]
    for i,(t,r,p,v) in enumerate(S):
        starts.append(off); ws=await one(i,t,r,p,v)
        d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f's{i}.mp3']))
        out+= [(o+off,du,w) for o,du,w in ws]
        subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f's{i}.mp3','-af',f'apad=pad_dur={gaps[i]}','-t',str(round(d+gaps[i],3)),'-ar','44100','-ac','1',f'p{i}.wav'])
        off+=d+gaps[i]; lst.append(f"file 'p{i}.wav'")
        print(i,round(d,2),round(off,2))
    json.dump(starts,open('starts.json','w'))
    open('l.txt','w').write("\n".join(lst))
    json.dump(out,open('words.json','w'))
asyncio.run(main())
