#used to store routes (basically webpages) for our website

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Listing, Biddings, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        x = current_user.first_name
    else:
        x = 'to SAUCTION!'
    return render_template("home.html", user=current_user, name=x)

@views.route('/user-listings', methods=['GET', 'POST'])
@login_required
def user_listings():
    return render_template("user_listings.html", user=current_user)

@views.route('/delete-listing', methods=['POST'])
def delete_note():
    listing = json.loads(request.data)
    listingID = listing['listingId']
    note = Listing.query.get(listingID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/market-listings')
@login_required
def market_listings():
    return render_template("market_listings.html", val=Listing.query.all(), user=current_user)

@views.route('/create-listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    if request.method == 'POST':
        itemName = request.form.get('itemname')
        desc = request.form.get('listing')
        baseprice = request.form.get('baseprice')
        if len(desc) < 1:
            flash('Please enter a valid item description!', category='error')
        elif len(itemName) < 1:
            flash('Please enter a valid Item Name!', category='error')
        else:
            new_listing = Listing(itemname=itemName, data=desc, bprice=baseprice, user_id=current_user.id)
            
            db.session.add(new_listing)
            db.session.commit()

            flash('Listing created!', category='success')
            return render_template("user_listings.html", user=current_user)
        
    return render_template("create_listing.html", user=current_user)

@views.route('/bidding-page/<itemid>', methods=['GET', 'POST'])
@login_required
def bidding(itemid):
    data = Listing.query.get(itemid)
    baseprice = data.bprice
    creatorid = data.user_id
    data2 = User.query.get(creatorid)

    data3 = Biddings.query.filter_by(listing_id=itemid).first()
    if data3:
        const = data3.amount
    else:
        const = 'No bids placed yet!'

    if request.method == 'POST':
        amount = request.form.get('bidAmount')
        bidentry = Biddings.query.filter_by(listing_id=itemid).first()
        if float(amount) < baseprice:
            flash('Bid amount must be greater than base price!', category='error')
        else:
            if bidentry:
                if float(amount) > bidentry.amount:
                    db.session.delete(bidentry)
                    newbid = Biddings(amount=amount, listing_id=itemid, user_id=current_user.id)
                    db.session.add(newbid)
                    db.session.commit()
                    flash('Bidding Added!', category='success')
                else:
                    flash('If you wish to bid, please enter a greater amount than the current highest bid!', category='error')
            else:
                newbid = Biddings(amount=amount, listing_id=itemid, user_id=current_user.id)
                db.session.add(newbid)
                db.session.commit()
                flash('Bidding Added!', category='success')

    return render_template("bidding_page.html", user=current_user, val=data, creator=data2, highest=const)

@views.route('/item-desc/<itemid>', methods=['GET', 'POST'])
@login_required
def item_desc(itemid):
    data = Listing.query.get(itemid)
    bid = Biddings.query.filter_by(listing_id=itemid).first()
    if bid:
        amt = bid.amount
        bidder = bid.user_id
        x = User.query.get(int(bidder))
        name = x.first_name + ' ' + x.last_name
    else:
        amt = 'No one has placed bids yet!'
        name = '-'
    return render_template("item_desc.html", user=current_user, val=data, amount=amt, name=name)