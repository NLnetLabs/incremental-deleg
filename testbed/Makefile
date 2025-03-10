ZONES = ideleg.net nsec3.ideleg.net customer1.ideleg.net customer1.nsec3.ideleg.net customer2.ideleg.net customer2.nsec3.ideleg.net customer3.ideleg.net customer3.nsec3.ideleg.net customer4.ideleg.net customer4.nsec3.ideleg.net deleg.net nsec3.deleg.net


all: $(ZONES:=.signed)

%: %.in
	./substitute.py $<

ideleg.net.signed: ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f $@.new -o $< - K$<.+013+60397 \
	&& mv $@.new $@

nsec3.ideleg.net.signed: nsec3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f $@.new -o $< - K$<.+013+52286 \
	&& mv $@.new $@

customer1.ideleg.net.signed: customer1.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f $@.new -o $< - K$<.+013+27601 \
	&& mv $@.new $@

customer1.nsec3.ideleg.net.signed: customer1.nsec3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f - -o $< - K$<.+013+06616 \
	| ldns-read-zone -u IDELEG > $@.new \
	&& mv $@.new $@

customer2.ideleg.net.signed: customer2.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f $@.new -o $< - K$<.+013+22597 \
	&& mv $@.new $@

customer2.nsec3.ideleg.net.signed: customer2.nsec3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f - -o $< - K$<.+013+39656 \
	| ldns-read-zone -u IDELEG > $@.new \
	&& mv $@.new $@

customer3.ideleg.net.signed: customer3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f $@.new -o $< - K$<.+013+62671 \
	&& mv $@.new $@

customer3.nsec3.ideleg.net.signed: customer3.nsec3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f $@.new -o $< - K$<.+013+11090 \
	&& mv $@.new $@

customer4.ideleg.net.signed: customer4.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f $@.new -o $< - K$<.+013+64041 \
	&& mv $@.new $@

customer4.nsec3.ideleg.net.signed: customer4.nsec3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f - -o $< - K$<.+013+24809\
	| ldns-read-zone -u IDELEG > $@.new \
	&& mv $@.new $@

deleg.net.signed: deleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f - -o $< - K$<.+013+54409 \
	| ldns-read-zone -u DELEG > $@.new \
	&& mv $@.new $@

nsec3.deleg.net.signed: nsec3.deleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f - -o $< - K$<.+013+13372 \
	| ldns-read-zone -u DELEG > $@.new \
	&& mv $@.new $@


sign:
	touch $(ZONES)
	$(MAKE)

resign:
	rm -f $(ZONES:=.signed)
	$(MAKE) sign

deploy-ideleg: ideleg.net.signed ideleg.net.conf
	scp ideleg.net.signed root@ideleg.net:/etc/nsd
	scp ideleg.net.conf root@ideleg.net:/etc/nsd/nsd.conf
	ssh root@ideleg.net nsd-control reconfig
	ssh root@ideleg.net nsd-control reload

deploy-supporting: customer1.ideleg.net.signed customer2.ideleg.net.signed customer3.ideleg.net.signed customer4.ideleg.net.signed nsec3.ideleg.net.signed supporting.conf
	scp customer1.ideleg.net.signed root@supporting.ideleg.net:/etc/nsd
	scp customer2.ideleg.net.signed root@supporting.ideleg.net:/etc/nsd
	scp customer3.ideleg.net.signed root@supporting.ideleg.net:/etc/nsd
	scp customer4.ideleg.net.signed root@supporting.ideleg.net:/etc/nsd
	scp nsec3.ideleg.net.signed root@supporting.ideleg.net:/etc/nsd
	scp supporting.conf root@supporting.ideleg.net:/etc/nsd/nsd.conf
	ssh root@supporting.ideleg.net nsd-control reconfig
	ssh root@supporting.ideleg.net nsd-control reload

deploy-nlnetlabs: nlnetlabs.conf customer3.nsec3.ideleg.net.signed
	scp customer3.nsec3.ideleg.net.signed root@ideleg.nlnetlabs.nl:/etc/nsd
	scp nlnetlabs.conf root@ideleg.nlnetlabs.nl:/etc/nsd/nsd.conf
	ssh root@ideleg.nlnetlabs.nl nsd-control reconfig
	ssh root@ideleg.nlnetlabs.nl nsd-control reload

deploy-legacy: legacy.conf customer1.nsec3.ideleg.net.signed customer2.nsec3.ideleg.net.signed customer3.nsec3.ideleg.net.signed
	scp customer1.nsec3.ideleg.net.signed root@legacy.ideleg.net:/etc/nsd
	scp customer2.nsec3.ideleg.net.signed root@legacy.ideleg.net:/etc/nsd
	scp customer4.nsec3.ideleg.net.signed root@legacy.ideleg.net:/etc/nsd
	scp legacy.conf root@legacy.ideleg.net:/etc/nsd/nsd.conf
	ssh root@legacy.ideleg.net nsd-control reconfig
	ssh root@legacy.ideleg.net nsd-control reload

deploy: deploy-ideleg deploy-supporting deploy-nlnetlabs deploy-legacy

